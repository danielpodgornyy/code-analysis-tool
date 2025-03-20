import math

class FunctionGrader():
    def __init__(self, functions):
        self.functions = functions

        self.penalties = 0 # Penalties are used to track each criterias failure and how much they do it

        self.failed_criteria = [] # Keys are the failed criteria and the results are an object of the message and criteria

        self.check_criteria()

    def check_criteria(self):
        """Iterates through each function within a file to collect the amount of penalties the file has accumulated per function"""

        for function in self.functions:
            function_body_text = ''
            # Add the lines to the function body
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

            # CRITERIA: IF THE CYCLOMATIC COMPLEXITY IS HIGH, IT SHOULD WARRANT A REFACTOR
            if self.calculate_cyclomatic_complexity(function_body_text) >= 10:
                self.penalties += 3
                self.failed_criteria.append({
                        'criteria': 'FUNCTIONTOOCOMPLEX',
                        'message': f"The function {function['name']} has a high cyclomatic complexity. This means that it has many paths that it goes down which can be difficult to follow. The code should be either seperated into functions or other structures or logic should be used instead",
                        'code': function['body']
                        })


    def calculate_cyclomatic_complexity(self, func_body):
        return func_body.count('if') + func_body.count('for') + func_body.count('while')

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
