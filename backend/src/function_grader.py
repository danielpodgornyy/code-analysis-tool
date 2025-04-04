import math
import re

class FunctionGrader():
    def __init__(self, functions):
        self.functions = functions

        self.penalties = 0 # Penalties are used to track each criterias failure and how much they do it

        self.failed_criteria = [] # Keys are the failed criteria and the results are an object of the message and criteria

        self.check_criteria()

    def check_criteria(self):
        """Iterates through each function within a file to collect the amount of penalties the file has accumulated per function"""

        for function in self.functions:

            # Add the lines to the function body (make is a string)
            function_body_text = ''
            for line in function['body']:
                function_body_text += line

            # CRITERIA: IF THE FUNCTION IS TOO SMALL, IT COULD WARRANT INLINING
            if len(function['body']) <= 3:
                self.penalties += 1
                self.failed_criteria.append({
                        'criteria': 'FUNCTIONTOOSHORT',
                        'message': f"The function {function['name']} appears to be a bit short. While this doesn't necessarily indicate an error, it could warrant just removing the function and replacing the call with the code itself.",
                        'code': function['body']
                        })


            # CRITERIA: IF THE FUNCTION IS TOO LONG, SPLIT IT UP INTO SMALLER FUNCTIONS
            if len(function['body']) >= 110:
                self.penalties += 3
                self.failed_criteria.append({
                        'criteria': 'FUNCTIONTOOLONG',
                        'message': f"The function {function['name']} appears to be a too long. While this doesn't necessarily indicate an error, it could mean that the function is handling too many tasks. It is generally considered best practice to split the function up into smaller functions that are called within the same function to improve readability.",
                        'code': function['body']
                        })

            # CRITERIA: IF THERE ARE TOO MANY PARAMS, GROUP PARAMS TOGETHER OR REFACTOR FUNCTION
            if len(function['params']) >= 6:
                self.penalties += 4
                self.failed_criteria.append({
                        'criteria': 'TOOMANYPARAMS',
                        'message': f"The function {function['name']} appears to have too many parameters. This could be an indication that the function handles too many tasks and in general it's hard to read and keep track of parameters if the amount becomes overbearing. The best course of action would be to either group together parameters using structs or any other data structure OR refactor the function as it could be handling too many tasks.",
                        'code': function['body']
                        })

            # CRITERIA: IF THE CYCLOMATIC COMPLEXITY IS HIGH, IT SHOULD WARRANT A REFACTOR
            if self.calculate_cyclomatic_complexity(function_body_text) >= 10:
                self.penalties += 5
                self.failed_criteria.append({
                        'criteria': 'FUNCTIONTOOCOMPLEX',
                        'message': f"The function {function['name']} has a high cyclomatic complexity. This means that it has many paths that it goes down which can be difficult to follow. The code should be either seperated into functions or other structures or logic should be used instead",
                        'code': function['body']
                        })

            # CRITERIA: TOO MANY LOCAL VARIABLES
            if self.count_local_variables(function['body']) > 10:
                self.penalties += 2
                self.failed_criteria.append({
                    'criteria': 'TOOMANYLOCALVARS',
                    'message': f"The function {function['name']} declares too many local variables. Simplify or refactor.",
                    'code': function['body']
                })

            # CRITERIA: DEEP NESTING
            if self.get_max_nesting_depth(function['body']) > 5:
                self.penalties += 3
                self.failed_criteria.append({
                    'criteria': 'DEEPNESTING',
                    'message': f"The function {function['name']} has deeply nested logic. Flatten or restructure.",
                    'code': function['body']
                })

            # CRITERIA: RANDOM NUMBER
            if self.find_magic_numbers(function['body']) > 5:
                self.penalties += 2
                self.failed_criteria.append({
                    'criteria': 'MAGICNUMBERS',
                    'message': f"The function {function['name']} uses several magic numbers. Use #define or consts instead.",
                    'code': function['body']
                })

    def calculate_cyclomatic_complexity(self, func_body):
        return func_body.count('if') + func_body.count('for') + func_body.count('while')

    def count_local_variables(self, body_lines):
        var_decl_pattern = re.compile(r'\b(int|float|double|char|long|short|unsigned|bool)\b\s+\**[a-zA-Z_][a-zA-Z0-9_]*')
        joined = '\n'.join(body_lines)
        return len(var_decl_pattern.findall(joined))

    def get_max_nesting_depth(self, body_lines):
        depth = max_depth = 0
        for line in body_lines:
            depth += line.count('{') - line.count('}')
            max_depth = max(max_depth, depth)
        return max_depth

    def find_magic_numbers(self, body_lines):
        # Ignores 1s and 0s
        magic_number_pattern = re.compile(r'\b(?!(?:0|1)\b)(\d+(\.\d+)?|\.\d+)\b')
        count = 0
        for line in body_lines:
            # Remove string literals
            line_no_strings = re.sub(r'"(\\.|[^"\\])*"', '', line)

            if line_no_strings.strip().startswith('#') or 'const' in line_no_strings:
                continue

            count += len(magic_number_pattern.findall(line_no_strings))
        return count


    def get_failed_criteria(self):
        return self.failed_criteria

    def calculate_file_grade(self, file_length):
        """Grades the individual file based on the penalties scaled by the size of the file"""

        # Find scaling factor
        scaling_factor = math.log(file_length + 1)

        # Scale penalties
        scaled_penalties = self.penalties / scaling_factor

        # Calculate final grade
        return max(0, round(100 - scaled_penalties, 2))




