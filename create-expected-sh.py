import sys
import os.path
import zipfile
from zipfile import ZipFile
import yaml
import json
from converter_utils import common_pref, list_testcases_with_testables, open_zip_from_argv


def main():
    if (len(sys.argv) < 2):
        print("usage: ./create-diffs-sh.py assignment.zip")
        return

    assignment = open_zip_from_argv(1)
    if (assignment is None):
        print("Error: unable to open zip file")
        return

    if (not (common_pref(assignment) + "project.yml") in assignment.namelist()):
        print("Error: project.yml missing")
        return

    project_desc = yaml.load(assignment.read(common_pref(assignment) + "project.yml"))

    formatted = "EXPECTED_FILES=\"%s\"" % " ".join([*project_desc["ExpectedFiles"]])
    with open('expected.sh', 'w') as expected:
        expected.write(formatted)

if __name__ == '__main__':
    main()