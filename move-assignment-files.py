import sys
import os.path
import zipfile
from zipfile import ZipFile
import yaml
from converter_utils import common_pref, list_testcases_with_testables, open_zip_from_argv

def copy_files_to_directory(filenames, directory, assignment):
    for filename in filenames:
        original_file =  assignment.read(common_pref(assignment) + filename).decode()
        os.makedirs(os.path.dirname(directory + "/" + filename), exist_ok=True)
        with open(directory + "/" + filename, "w") as moved_file:
            moved_file.write(original_file)

def main():
    if (len(sys.argv) < 2):
        print("usage: ./create-diffs-sh.py assignment.zip")
        return

    zip_path = sys.argv[1]

    if (not os.path.isfile(zip_path)):
        print("Error: %s is not a valid file" % zip_path)
        return

    assignment = open_zip_from_argv(1)
    if (assignment is None):
        print("Error: unable to open zip file")
        return
            
    if (common_pref(assignment) + "Makefile" in assignment.namelist()):
        makefile = assignment.read(common_pref(assignment) + "Makefile")
        with open("BUILD-FILES/Makefile", "w") as moved_makefile:
            moved_makefile.write(makefile.decode())
    
    execution_files = {}
    build_files = {}
    for test_case, testable in list_testcases_with_testables(assignment):
        for f in testable["ExecutionFiles"]:
            execution_files["execution_files/" + f] = True
        if ("Input" in test_case):
            execution_files[test_case["Input"]["File"]] = True
        for f in testable["BuildFiles"]:
            build_files["build_files/" + f] = True

    copy_files_to_directory([*execution_files], "EXECUTION-FILES", assignment)
    copy_files_to_directory([*build_files], "BUILD-FILES", assignment)


if __name__ == '__main__':
    main()
