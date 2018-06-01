import sys
import os.path
import zipfile
from zipfile import ZipFile
import yaml
import json
from converter_utils import list_testcases_with_testables, open_zip_from_argv

def test_case_to_bash_format(test_case, testable):
    test_spec = {}
    if (test_case["Output"]["Source"] in ["stdout", "stderr"]):
        test_spec[test_case["Output"]["Source"]] = test_case["Points"]
    else:
        test_spec["filename"] = test_case["Output"]["Source"]
        test_spec["points"] = test_case["Points"]

    if (testable["IsHidden"]):
        test_spec["visibility"] = "hidden"

    if (("HideExpected" in test_case) and test_case["HideExpected"]):
        test_spec["hide_expected"] = True

    bash_cmd = test_case["Command"]
    print(test_case)

    if ("Input" in test_case):
        bash_cmd += " < \"" + test_case["Input"]["File"] + "\""

    #Some tests on Submit call the test binary as though
    #it were in the path. (e.g. testprog instead of ./testprog)
    #This allows those tests to run correctly
    if (not test_case["Command"].startswith("./")):
        bash_cmd = "env PATH=$PATH:$(pwd) " + bash_cmd

    return "#@test" + json.dumps(test_spec) + "\n" + bash_cmd

def main():
    if (len(sys.argv) < 2):
        print("usage: ./create-diffs-sh.py assignment.zip")
        return

    assignment = open_zip_from_argv(1)
    if (assignment is None):
        print("Error: unable to open zip file")
        return

    #Clear diffs.sh
    with open('diffs.sh', 'w') as diffs:
        pass

    for test_case, testable in list_testcases_with_testables(assignment):
        formatted = test_case_to_bash_format(test_case, testable)
        with open('diffs.sh', 'a') as diffs:
            diffs.write(formatted)
            diffs.write("\n\n")

if __name__ == '__main__':
    main()