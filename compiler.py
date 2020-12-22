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
    'java11': {
        'docker_image': 'stepik/epicbox-java:11.0.1',
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

        result = (epicbox.run('gcc_run', './main',
                              limits={'cputime': 2, 'memory': 64},
                              workdir=workdir))
    return result


def execute_java(code, name_of_class):
    files = [{'name': f'{name_of_class}.java', 'content': code}]
    limits = {'cputime': 2, 'memory': 64}
    result = epicbox.run('java11', f'javac {name_of_class}.java; java {name_of_class}', files=files,
                         limits=limits)
    return result


def execute_python(code):
    files = [{'name': 'main.py', 'content': code}]
    limits = {'cputime': 2, 'memory': 64}
    result = epicbox.run('python', 'python3 main.py', files=files, limits=limits)
    return result


def format_result(response):
    exit_code = response['exit_code']  # Integer
    stdout = response['stdout'].decode('utf-8')  # String
    stderr = response['stderr'].decode('utf-8')  # String
    duration = response['duration']  # Float
    timeout = response['timeout']  # Boolean
    oom_killed = response['oom_killed']  # Boolean

    result = 'exit_code: ' + str(
        exit_code) + '\n' + 'stdout: ' + stdout + '\n' + 'stderr: ' + stderr + '\n' + 'duration: ' + str(
        duration) + '\n' + 'timeout: ' + str(timeout) + '\n' + 'oom_killed: ' + str(oom_killed) + '\n'
    return result


def compile_text(text, language):
    code = text.encode('UTF-8')
    response = ''
    if language == 'C++':
        response = execute_cpp(code)
    elif language == 'Java':
        text = text.split()
        name_of_class = text[text.index('class') + 1].replace('{', '')
        response = execute_java(code, name_of_class)
    elif language == 'Python':
        response = execute_python(code)

    result = format_result(response)
    return result
