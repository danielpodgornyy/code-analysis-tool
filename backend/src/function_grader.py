import math

class FunctionGrader():
    def __init__(self, functions):
        self.functions = functions

        self.penalties = 0 # Penalties are used to track each criterias failure and how much they do it

        self.failed_criteria = [] # Keys are the failed criteria and the results are an object of the message and criteria

        raw_penalties = self.check_criteria()

    def check_criteria(self):
        for function in self.functions:
            # CRITERIA: IF THE FUNCTION IS TOO SMALL, IT COULD WARRANT INLINING
            if len(function['body']) <= 3:
                self.penalties += 1
                self.failed_criteria.append({
                        'criteria': 'FUNCTIONTOOSHORT',
                        'message': f"The function {function['name']} appears to be a bit short. While this doesn't necessarily indicate an error, it could warrant just removing the function and replacing the call with the code itself.",
                        'code': function['body']
                        })

    def get_failed_criteria(self):
        return self.failed_criteria

    def calculate_file_grade(self, file_length):
        # Find scaling factor
        scaling_factor = math.log(file_length + 1)

        # Scale penalties
        scaled_penalties = self.penalties / scaling_factor

        # Calculate final grade
        return max(0, 100 - scaled_penalties)






