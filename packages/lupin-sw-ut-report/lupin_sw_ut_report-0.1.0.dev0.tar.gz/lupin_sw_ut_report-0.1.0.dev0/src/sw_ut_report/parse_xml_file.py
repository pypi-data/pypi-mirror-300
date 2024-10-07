import xml.etree.ElementTree as ET
from datetime import datetime
from os import PathLike
from typing import Dict

from sw_ut_report.template_manager import get_local_template
from sw_ut_report.utils import remove_excess_space

PASS = "🟢 PASS"
FAIL = "❌ FAIL"
NA = "⚪ N/A"


def format_testcase_name(testcase: ET.Element) -> str:
    testcase_name = remove_excess_space(testcase.attrib.get("name")).replace("::", ": ")
    testcase_name_split = testcase_name.split(":")
    if len(testcase_name_split) > 1:
        testcase_name = (
            f"**{testcase_name_split[0].strip()}**: {','.join(testcase_name_split[1:])}"
        )
    return testcase_name.strip()


def get_formatted_timestamp(testsuites_id: str) -> str:
    try:
        timestamp = datetime.strptime(testsuites_id, "%Y %m %d %H:%M:%S")
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        formatted_timestamp = testsuites_id
    return formatted_timestamp


def if_failures(testsuites_failures: str) -> str:
    return FAIL if int(testsuites_failures) > 0 else PASS


def format_xml_to_dict(xml_file: PathLike) -> Dict:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract information from the first level "testsuites"
    testsuites_name = root.attrib.get("name")
    testsuites_id = root.attrib.get("id")
    testsuites_tests = root.attrib.get("tests")
    testsuites_errors = root.attrib.get("errors")
    testsuites_failures = root.attrib.get("failures")

    # Détermination du statut PASS ou FAIL
    status = if_failures(testsuites_failures)

    testsuites_dict = {
        "name": testsuites_name,
        "timestamp": get_formatted_timestamp(testsuites_id),
        "tests": testsuites_tests,
        "errors": testsuites_errors,
        "failures": testsuites_failures,
        "status": status,
        "suites": [],
    }

    # Browse each "testsuite" in "testsuites"
    for testsuite in root.findall("testsuite"):
        testsuite_name = testsuite.attrib.get("name")
        testsuite_tests = testsuite.attrib.get("tests")
        testsuite_failures = testsuite.attrib.get("failures")
        status_suite = if_failures(testsuite_failures)

        testsuite_dict = {
            "name": testsuite_name,
            "tests": testsuite_tests,
            "failures": testsuite_failures,
            "status": status_suite,
            "testcases": [],
        }

        # Browse each "testcase" in "testsuite"
        for testcase in testsuite.findall("testcase"):
            testcase_name = format_testcase_name(testcase)
            testcase_tests = testcase.attrib.get("tests", "N/A")
            testcase_failures = testcase.attrib.get("failed", "N/A")
            if testcase_failures == "N/A":
                status_test = NA
            else:
                status_test = if_failures(testcase_failures)

            testcase_dict = {
                "name": testcase_name,
                "tests": testcase_tests,
                "failures": testcase_failures,
                "status": status_test,
            }
            testsuite_dict["testcases"].append(testcase_dict)

        testsuites_dict["suites"].append(testsuite_dict)

    return testsuites_dict


def convert_markdown_from_xml(input_file: PathLike, output_file: PathLike) -> None:
    template = get_local_template("test_report_xml_to_markdown.j2")

    data = format_xml_to_dict(input_file)
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(template.render(testsuites=data))
