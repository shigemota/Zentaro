import os.path, subprocess
from subprocess import STDOUT, PIPE
import subprocess


def execute_cpp(directory):
    s = subprocess.check_output(
        f"g++ {directory}/Main.cpp -o {directory}/Main;.{directory}/Main", shell=True)
    result = s.decode("utf-8")
    return result


def execute_java(directory):
    s = subprocess.check_output(
        f"javac {directory};java {directory}", shell=True)
    result = s.decode("utf-8")
    return result


def execute_python(directory):
    s = subprocess.check_output(
        f"python3 {directory}/Main.py", shell=True)
    return s.decode("utf-8")


def main(text, language):
    extensions = {'C++': 'cpp', 'Java': 'java', 'Python': 'py'}
    file = 'Main.'
    file += extensions[language]

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, file)

    open(abs_file_path, 'w').close()
    f = open(abs_file_path, "a")
    for words in text:
        f.write(words + '\n')
    f.close()
    if language == 'C++':
        return execute_cpp(script_dir)
    elif language == 'Java':
        return execute_java(abs_file_path)
    elif language == 'Python':
        return execute_python(script_dir)

# Driver function
# if __name__ == "__main__":
#     print(main('''print("123")''', 'Python'))
# execute_cpp()
# execute_java()
