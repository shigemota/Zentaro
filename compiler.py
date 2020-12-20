import epicbox

PROFILES = {
    'gcc_compile': {
        'docker_image': 'stepik/epicbox-gcc:6.3.0',
        'user': 'root',
    },
    'gcc_run': {
        'docker_image': 'stepik/epicbox-gcc:6.3.0',
        # It's safer to run untrusted code as a non-root user (even in a container)
        'user': 'sandbox',
        'read_only': True,
        'network_disabled': False,
    },
    'python': {
        'docker_image': 'python:3.6.5-alpine',
    }
}
epicbox.configure(profiles=PROFILES)


def execute_cpp(code):
    with epicbox.working_directory() as workdir:
        epicbox.run('gcc_compile', 'g++ -pipe -O2 -static -o main main.cpp',
                    files=[{'name': 'main.cpp', 'content': code}],
                    workdir=workdir)
        print(epicbox.run('gcc_run', './main', stdin='2 2',
                          limits={'cputime': 1, 'memory': 64},
                          workdir=workdir))
        # {'exit_code': 0, 'stdout': b'4\n', 'stderr': b'', 'duration': 0.095318, 'timeout': False, 'oom_killed': False}

        result = (epicbox.run('gcc_run', './main', stdin='14 5',
                              limits={'cputime': 1, 'memory': 64},
                              workdir=workdir))
    return result


def execute_java(code):
    return "TODO ADD JAVA"


def execute_python(code):
    files = [{'name': 'main.py', 'content': code}]
    limits = {'cputime': 1, 'memory': 64}
    result = epicbox.run('python', 'python3 main.py', files=files, limits=limits)
    return result


def format_result(response):
    exit_code = response['exit_code']  # Integer
    stdout = response['stdout'].decode('utf-8')  # String
    stderr = response['stderr'].decode('utf-8')  # String
    duration = response['duration']  # Float
    timeout = response['timeout']  # Boolean

    result = 'Stdout: ' + stdout + '\n' + 'Duration: ' + str(duration) + '\n' + 'Timeout: ' + str(timeout) + '\n'
    return result


def compile_text(text, language):
    text = text.encode('UTF-8')
    response = ''
    if language == 'C++':
        response = execute_cpp(text)
    elif language == 'Java':
        response = execute_java(text)
    elif language == 'Python':
        response = execute_python(text)
    print(response)

    result = format_result(response)
    print(result)
    return result

# if __name__ == "__main__":
#     (compile_text('''
# #include<iostream>
# using namespace std;
# int main(){
#     int a,b;
#     cin >> a >> b;
#     cout << a + b << endl;
# }
# ''', 'C++'))
