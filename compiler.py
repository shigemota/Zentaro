import epicbox

# import logging

# logging.basicConfig(
#     format="%(levelname)-8s [%(asctime)s] %(message)s",
#     level=logging.INFO,
#     filename="app.log",
# )

PROFILES = {
    "gcc_compile": {
        "docker_image": "stepik/epicbox-gcc:6.3.0",
        "user": "root",
    },
    "gcc_run": {
        "docker_image": "stepik/epicbox-gcc:6.3.0",
        "user": "sandbox",
        "read_only": True,
        "network_disabled": False,
    },
    "java": {
        "docker_image": "stepik/epicbox-java:11.0.1",
    },
    "python": {
        "docker_image": "python:3.6.5-alpine",
    },
}
epicbox.configure(profiles=PROFILES)


def execute_cpp(untrusted_code, input_values, limits):
    result = []
    with epicbox.working_directory() as workdir:
        value = epicbox.run(
            "gcc_compile",
            "g++ -pipe -O2 -static -o main main.cpp",
            files=[{"name": "main.cpp", "content": untrusted_code}],
            workdir=workdir,
        )
        if value["stderr"]:
            return [value]

        for val in input_values:
            result.append(
                epicbox.run(
                    "gcc_run",
                    "./main",
                    stdin=val,
                    limits=limits,
                    workdir=workdir,
                )
            )
    return result


def execute_java(untrusted_code, input_values, limits):
    result = []
    with epicbox.working_directory() as workdir:
        text = untrusted_code.decode("UTF-8")
        text = text.split()
        name_of_class = text[text.index("class") + 1].replace("{", "")
        files = [{"name": f"{name_of_class}.java", "content": untrusted_code}]

        value = epicbox.run(
            "java",
            f"javac {name_of_class}.java",
            files=files,
            workdir=workdir,
            limits=limits,
        )
        if value["stderr"]:
            return [value]

        for val in input_values:
            result.append(
                epicbox.run(
                    "java",
                    f"java {name_of_class}",
                    files=files,
                    workdir=workdir,
                    stdin=val,
                    limits=limits,
                )
            )
    return result


def execute_python(untrusted_code, input_values, limits):
    result = []
    with epicbox.working_directory() as workdir:
        files = [{"name": "main.py", "content": untrusted_code}]
        for val in input_values:
            result.append(
                epicbox.run(
                    "python",
                    "python3 main.py",
                    files=files,
                    workdir=workdir,
                    stdin=val,
                    limits=limits,
                )
            )
    return result


def format_result(response):
    exit_code = response["exit_code"]  # Integer
    stdout = response["stdout"].decode("utf-8")  # String
    stderr = response["stderr"].decode("utf-8")  # String
    duration = response["duration"]  # Float
    timeout = response["timeout"]  # Boolean
    oom_killed = response["oom_killed"]  # Boolean

    if stderr:
        result = stderr
    else:
        result = stdout

    # result = (
    #     "exit_code: "
    #     + str(exit_code)
    #     + "\n"
    #     + "stdout: "
    #     + stdout
    #     + "\n"
    #     + "stderr: "
    #     + stderr
    #     + "\n"
    #     + "duration: "
    #     + str(duration)
    #     + "\n"
    #     + "timeout: "
    #     + str(timeout)
    #     + "\n"
    #     + "oom_killed: "
    #     + str(oom_killed)
    #     + "\n"
    # )
    return result


def compile_text(text, language, input_values=None, limits=None, output_values=None):
    if limits is None:
        limits = {"cputime": 2, "memory": 64}
    if input_values is None:
        input_values = [""]
    if output_values is None:
        output_values = [""]

    untrusted_code = text.encode("UTF-8")
    response = ""
    if language == "C++":
        response = execute_cpp(untrusted_code, input_values, limits)
    elif language == "Java":
        response = execute_java(untrusted_code, input_values, limits)
    elif language == "Python":
        response = execute_python(untrusted_code, input_values, limits)

    result = ""
    for index, res in enumerate(response):

        out = output_values[index]
        inp = format_result(res)

        compare_output = (inp == out)

        result += (
                "Output #" + str(index + 1) + " - " + str(compare_output) + '\n' + format_result(res) + "\n"
        )

    return result
