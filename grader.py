import sys
import glob
import os
import shutil

if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

def start_grade(path_to_names, path_to_submissions, template_path, testdata_path):
    name_list = read_names(path_to_names);
    name_files_dict = pick_corresponding_files(name_list, path_to_submissions)
    name_testfile_dict = generate_test_files(name_list, name_files_dict, template_path, testdata_path)

    grade_all(name_files_dict, name_testfile_dict)

def read_names(path_to_names):
    names = []
    with open(path_to_names, 'r') as name_file:
        lines = name_file.readlines()
        for line in lines:
            names.append(line.strip())
    return names

def pick_corresponding_files(name_list, path_to_submissions):
    name_files_dict = {}
    for name in name_list:
        files = glob.glob(path_to_submissions + "/" + name + "_" +"*.py")
        name_files_dict[name] = files
    return name_files_dict

def generate_test_file(student_name, name_files_dict, template_path, testdata_path, output_path):
    with open(output_path, 'w') as test_file:
        #Here, we only pick the first file as the final version of student's submission if there are multiple files
        if len(name_files_dict[student_name]) > 0:
            file_path = name_files_dict[student_name][0]
            test_file.write("import imp\n")
            test_file.write("imp.load_source('current_stud', '{}')\n".format(file_path))
            test_file.write("from current_stud import *\n")

            #Embed template file
            template_file = open(template_path, 'r')
            test_file.write(''.join(template_file.readlines()))
            template_file.close()

            #Embed testdata file
            testdata_file = open(testdata_path, 'r')
            test_file.write(''.join(testdata_file.readlines()))
            testdata_file.close()

            test_file.write("\nif __name__ == '__main__':\n\ttest(debug=True)\n")
        else:
            test_file.write("This student has no submission!\n")

def generate_test_files(name_list, name_files_dict, template_path, testdata_path):
    if os.path.exists("test"):
        shutil.rmtree("test")
    os.mkdir("test")

    name_testfile_dict = {}

    for name in name_list:
        output_path = os.path.abspath("test/" + name + ".py")
        generate_test_file(name, name_files_dict, template_path, testdata_path, output_path)
        name_testfile_dict[name] = output_path

    return name_testfile_dict

def grade_student(student_name, name_files_dict, name_testfile_dict, output_path):
    print "Grading " + student_name + "..."
    test_file = name_testfile_dict[student_name]
    try:
        out = subprocess.check_output(["python", test_file],
                                      stderr=subprocess.STDOUT, universal_newlines=True, timeout=5)
    except subprocess.CalledProcessError as e:
        out = e.output
    except subprocess.TimeoutExpired as timeout:
        print "Times out!"
        out = "Times out! There may be some infinite loop in the program"
    with open(output_path, 'w') as out_file:
        out_file.write(out)

        if (len(name_files_dict[student_name]) > 0):
            src_code = open(name_files_dict[student_name][0], 'r')
            out_file.write('\n------------------------\nSource Code: \n')
            out_file.write(''.join(src_code.readlines()))
            src_code.close()


def grade_all(name_files_dict, name_testfile_dict):
    if os.path.exists("reports"):
        shutil.rmtree("reports")
    os.mkdir("reports")
    for name in name_testfile_dict:
        output_path = os.path.abspath("reports/" + name + ".txt")
        grade_student(name, name_files_dict, name_testfile_dict, output_path)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'wrong usage'
        sys.exit(1)

    path_to_names = os.path.abspath(sys.argv[1])
    path_to_submissions = os.path.abspath(sys.argv[2])
    template_path = os.path.abspath(sys.argv[3])
    testdata_path = os.path.abspath(sys.argv[4])

    start_grade(path_to_names, path_to_submissions, template_path, testdata_path)
