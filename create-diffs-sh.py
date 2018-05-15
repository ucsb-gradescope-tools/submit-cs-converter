import sys
import os.path
import zipfile
from zipfile import ZipFile
import yaml
import json

def list_testables(assignment):
    testables = {}
    for name in assignment.namelist():
        if name.startswith("testables/"):
            testables[name.split("/")[1]] = True

    return [*testables]

def test_case_to_bash_format(test_case, testable):
    test_spec = {}
    if (test_case["Output"]["Source"] in ["stdout", "stderr"]):
        test_spec[test_case["Output"]["Source"]] = test_case["Points"]
    else:
        test_spec["filename"] = test_case["Output"]["Source"]
        test_spec["points"] = test_case["Points"]

    if (testable["IsHidden"]):
        test_spec["visibility"] = "hidden"

    bash_cmd = test_case["Command"]

    if ("Input" in test_case):
        bash_cmd += " < \"" + "/".join(test_case["Input"]["File"].split("/")[1:]) + "\""

    return json.dumps(test_spec) + "\n" + bash_cmd

def main():
    if (len(sys.argv) < 2):
        print("usage: ./create-diffs-sh.py assignment.zip")
        return

    zip_path = sys.argv[1]

    if (not os.path.isfile(zip_path)):
        print("Error: %s is not a valid file" % zip_path)
        return

    try:
        with ZipFile(zip_path) as assignment:
            if (not "project.yml" in assignment.namelist()):
                print("Error: project.yml is missing")
                return
            project_desc = assignment.read("project.yml")
            
            #Clear diffs.sh
            with open('diffs.sh', 'w') as diffs:
                pass

            for testable in list_testables(assignment):
                description_path = "testables/" + testable + "/" + testable + ".yml"
                if (not description_path in assignment.namelist()):
                    print("Error: %s is missing" % description_path) 

                testable_desc = yaml.load(assignment.read(description_path))
                for test_case in testable_desc["TestCases"]:
                    formatted = test_case_to_bash_format(testable_desc["TestCases"][test_case], testable_desc)
                    with open('diffs.sh', 'a') as diffs:
                        diffs.write(formatted)
                        diffs.write("\n\n")

    except zipfile.BadZipFile as e:
        print("Bad zip file")
        return

if __name__ == '__main__':
    main()