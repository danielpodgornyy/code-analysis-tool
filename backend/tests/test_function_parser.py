import pytest
import tempfile
from src.function_parser import FunctionParser

def test_function_parser_extracts_function_correctly():
    c_code = """
    int add(int a, int b) {
        return a + b;
    }

    void greet() {
        printf("Hello!");
    }
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".c", mode="w") as temp_c_file:
        temp_c_file.write(c_code)
        temp_c_file_path = temp_c_file.name

    parser = FunctionParser(temp_c_file_path)
    functions = parser.get_functions()
    assert len(functions) == 2
    assert functions[0]["name"] == "add"
    
    assert "return a + b;" in "".join(functions[0]["body"])
    assert functions[1]["name"] == "greet"
    
