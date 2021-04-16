from flask import Flask, jsonify
from flask import render_template, request
from compiler.compiler import compile_code
from database.db import *

app = Flask(__name__)


@app.route("/background_process")
def background_process():
    text = (request.args.get("proglang", 0, type=str)).encode("UTF-8")
    lang = request.args.get("lang", 0, type=str)
    problem = request.args.get("problem", 0, type=str)

    problem_data = get_from_problems_db(problem)
    problem_limit = float(problem_data['limits']['time'])
    problem_tests = problem_data['tests']
    limits = {"limit": {"time": problem_limit}}

    problem = []
    for i in range(len(problem_tests)):
        inp_out = problem_tests[i]
        for j in range(len(inp_out)):
            inp_out[j] = inp_out[j].encode("UTF-8")
        problem.append(tuple(inp_out))

    result = compile_code(text, lang, problem, limits)
    return jsonify(result=str(result))


@app.route("/")
def code_editor():
    languages = ["Java", "C++", "Python 3"]  # Todo: Add all languages

    data = []
    for lang in languages:
        data.append({"name": lang})

    return render_template("index.html", data=data)


@app.route("/success")
def success():
    return "success"


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
