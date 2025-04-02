import pytest
from src.function_grader import FunctionGrader

def test_grader_flags_short_function():
    functions = [
        {'name': 'short_func', 'params': ['int a'], 'body': ['int x = a;', 'return x;']}
    ]
    grader = FunctionGrader(functions)
    failed = grader.get_failed_criteria()

    assert any(f['criteria'] == 'FUNCTIONTOOSHORT' for f in failed)

def test_grader_flags_long_function():
    body = ["line;\n"] * 111
    functions = [{'name': 'long_func', 'params': ['int a'], 'body': body}]
    grader = FunctionGrader(functions)
    failed = grader.get_failed_criteria()

    assert any(f['criteria'] == 'FUNCTIONTOOLONG' for f in failed)

def test_grader_flags_many_params():
    functions = [{'name': 'param_func', 'params': ['int a', 'int b', 'int c', 'int d', 'int e', 'int f'], 'body': ['return;']}]
    grader = FunctionGrader(functions)
    failed = grader.get_failed_criteria()

    assert any(f['criteria'] == 'TOOMANYPARAMS' for f in failed)

def test_grader_flags_complex_function():
    functions = [{'name': 'complex_func', 'params': ['int x'], 'body': ['if(x){}', 'for(int i=0;i<5;i++){}', 'while(x){}'] * 5}]
    grader = FunctionGrader(functions)
    failed = grader.get_failed_criteria()

    assert any(f['criteria'] == 'FUNCTIONTOOCOMPLEX' for f in failed)

def test_calculate_file_grade():
    functions = [{'name': 'basic', 'params': [], 'body': ['return;']}]
    grader = FunctionGrader(functions)
    grade = grader.calculate_file_grade(100)
    assert isinstance(grade, float)
    assert 0 <= grade <= 100
