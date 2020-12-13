import subprocess
import os


def execute_cpp():
    # create a pipe to a child process
    data, temp = os.pipe()
    # write to STDIN as a byte object(convert string
    # to bytes with encoding utf8)
    os.write(temp, bytes("5 10\n", "utf-8"))
    os.close(temp)
    # store output of the program as a byte string in s
    s = subprocess.check_output(
        "g++ main.cpp -o out2;./out2", stdin=data, shell=True)
    # decode s to a normal string
    os.remove("out2")
    return s.decode("utf-8")


def execute_java():
    # store the output of
    # the java program
    s = subprocess.check_output(
        "javac Main.java;java Main", shell=True)
    os.remove("Main.class")
    return s.decode("utf-8")


def execute_python():
    s = subprocess.check_output(
        "python3 main.py", shell=True)
    return s.decode("utf-8")


def main(text, language):
    extensions = {'C++': 'cpp', 'Java': 'java', 'Python': 'py'}
    file = 'main.' if language == 'C++' or 'Python' else 'Main.'
    file += extensions[language]
    open(file, 'w').close()
    f = open(file, "a")
    for words in text:
        f.write(words)
    f.close()
    if language == 'C++':
        return execute_cpp()
    elif language == 'Java':
        return execute_java()
    elif language == 'Python':
        return execute_python()

# Driver function
# if __name__ == "__main__":
#     main('''n = 100
# factorial = 1
# if int(n) >= 1:
# for i in range (1,int(n)+1):
#    factorial = factorial * i
# print("Factorail of ",n , " is : ",factorial)''', 'Python')
# execute_cpp()
# execute_java()
