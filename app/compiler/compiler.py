from dockerjudge import judge
from dockerjudge.processor import (
    GCC,
    Clang,
    Bash,
    Python,
    Node,
    OpenJDK,
    PHP,
    Ruby,
    Mono,
    Swift,
)


def format_result(output_result):
    pass


def compile_code(code, lang, test_values=None, limits=None):
    language_classes = {
        "C++": GCC(GCC.Language.cpp),
        "Java": OpenJDK(),
        "Python 3": Python(3),
    }
    lang = language_classes[lang]
    result = judge(lang, code, test_values, limits)
    return result
