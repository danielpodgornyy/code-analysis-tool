import re

class FunctionParser():
    def __init__(self, file_path):
        self.lines = []
        self.functions = []

        self.parse(file_path)

    def parse(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            self.lines = file.readlines()

        self.extract_function_bodies()

    def extract_function_bodies(self):
        # Regex to match the start of a function and get its name
        func_name_pattern = r"\b(?:unsigned\s+)?(?:short|int|long|float|double|char|void)\s+([\w_]+)\s*\([^)]*\)\s*(?=\{)"
        # Regex to match either a left or right bracket
        brackets_pattern = r"\{|\}"

        bracket_stack = []
        current_function_name = None
        # temp_func used to keep track of function contents and is used to append to the functions array
        temp_func = {
                'name': None,
                'parameters': [],
                'body': []
                }
        for line in self.lines:
            # Skip empty lines
            if (line.strip() == ""):
                continue

            # If the line matches the regex for a function signature we are inside a function
            func_match = re.search(func_name_pattern, line)
            if func_match:
                current_function_name = func_match.group(1)
                temp_func['name'] = current_function_name
                temp_func['params'] = self.parse_params(func_match.group(0))
                temp_func['body'] = []
                bracket_stack.append("{")
                continue

            # For every bracket in the line, we append and pop for each corresponding opening and closing bracket
            brackets = re.findall(brackets_pattern, line)
            for bracket in brackets:
                if bracket == '{':
                    bracket_stack.append("{")
                elif bracket == '}':
                    bracket_stack.pop()

            # If we're in a function, add the line to the functions structure under the current function name
            if current_function_name and bracket_stack:
                temp_func['body'].append(line)

            # If the function has ended, clear the function name
            if current_function_name and not bracket_stack:
                self.functions.append(temp_func)
                current_function_name = None

    def parse_params(self, func_signature):
        param_string = func_signature.split('(', 1)[-1].split(')', 1)[0]
        param_list = param_string.split(', ')
        return param_list

    def get_functions(self):
        return self.functions

    def get_file_length(self):
        return len(self.lines)
