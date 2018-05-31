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

    if (test_case["HideExpected"]):
        test_spec["hide_expected"] = True

    bash_cmd = test_case["Command"]
    print(test_case)

    if ("Input" in test_case):
        bash_cmd += " < \"" + test_case["Input"]["File"] + "\""

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