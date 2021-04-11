from flask import Flask, jsonify
from flask import render_template, request
from compiler.compiler import compile_code

app = Flask(__name__)


@app.route("/background_process")
def background_process():
    text = (request.args.get("proglang", 0, type=str)).encode("UTF-8")
    lang = request.args.get("lang", 0, type=str)
    problem = request.args.get("problem", 0, type=int)

    problems = {
        1: [(b"2 3", b"5"), (b"190 23", b"213")],
        2: [(b"2 3", b"5"), (b"190 23", b"213")],
    }

    limit = request.args.get("limits", 0, type=float)
    limits = {"limit": {"time": limit}}

    result = compile_code(text, lang, problems[problem], limits)
    print("Finished Compiling")
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
