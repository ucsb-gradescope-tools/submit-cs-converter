import sys
import os.path
import zipfile
from zipfile import ZipFile
import yaml
import json

def list_testable_names(assignment):
    testables = {}
    for name in assignment.namelist():
        if name.startswith("testables/"):
            testables[name.split("/")[1]] = True

    return [*testables]

def list_testcases_with_testables(assignment):
    retval = []

    for testable in list_testable_names(assignment):
        description_path = "testables/" + testable + "/" + testable + ".yml"
        if (not description_path in assignment.namelist()):
            print("Error: %s is missing" % description_path)
            continue

        testable_desc = yaml.load(assignment.read(description_path))
        for test_case in testable_desc["TestCases"]:
            retval.append((testable_desc["TestCases"][test_case], testable_desc))

    return retval

def open_zip_from_argv(arg_position):
    if (len(sys.argv) <= arg_position):
        return None

    zip_path = sys.argv[1]

    if (not os.path.isfile(zip_path)):
        print("Error opening zip: %s is not a valid file" % zip_path)
        return None

    try:
        return ZipFile(zip_path)
    except zipfile.BadZipFile:
        print("Error: Bad zip file")
        return