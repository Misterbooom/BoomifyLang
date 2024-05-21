from exceptions import VariableError,TypeError
from type.interpreter_type import InterpreterType

from icecream import ic
class VariableManager:
    def __init__(self, interpreter: InterpreterType):
        self.vars = {}
        self.interpreter = interpreter
        self.vars_type = {
            "str": [("'", "'"), ('"', '"')],
            "tuple": [("(", ")")],
            "list": [("[", "]")],
        }
        self.func_count = 0
    def variable_assignment(self, var_name: str = None, var_value: str = None):

        var_type = self.check_var_type(var_value)
        self.interpreter.log("Type Setting", f"Type set to {var_type} for {var_value}")
        if var_name :
            self.check_correct_var_name(var_name)
        if not var_type:
            self.interpreter.raise_error(
                VariableError, "Invalid variable type", var_value
            )
        var_value = self.parse_value(var_type, var_value)
        
        if var_name:
            self.vars[var_name] = var_value
            self.interpreter.log("Variables", self.vars)
            self.interpreter.log(var_name, f"Assigned {var_value} to {var_name}")
            
        return var_value

    def check_var_type(self, var_value: str): 
        ic(var_value)
        if self.interpreter.func_manager.get_function(var_value,True,False):
            return "function"

        if var_value == "[]":
            return "list"
        elif var_value == "()":
            return "tuple"
        if var_value.startswith("-") and var_value[1:].isdigit():
            return "int"  
        if var_value.isdigit():
            return "int"
        if var_value.startswith("-") and var_value[1:].replace(".", "", 1).isdigit():
            return "float"  
            
        if var_value.replace(".", "", 1).isdigit():
            return "float"

        for var_type, valid_chars in self.vars_type.items():
            for valid_char in valid_chars:
                valid_start, valid_end = valid_char
                if var_value.startswith(valid_start) and var_value.endswith(valid_end):
                    self.interpreter.log(
                        "Type Check", f"Type {var_type} identified for {var_value}"
                    )
                    return var_type
        self.func_count = 0
        return None
    def parse_value(self,var_type:str, var_value: str):
        try:
            if var_type == "int":
                var_value = int(var_value)
            elif var_type == "float":
                var_value = float(var_value)
            elif var_type == "str":
                var_value = var_value.strip('"').strip("'")
            elif var_type == "tuple":
                var_value = self.collection_assignment(var_value, tuple)
            elif var_type == "list":
                var_value = self.collection_assignment(var_value, list)
            elif var_type == "function":
                var_value = self.interpreter.func_manager.get_function(var_value.replace('call ', ''))
            return var_value
                
        except SyntaxError as e:
            self.interpreter.raise_error(
                VariableError, f"Invalid variable value, {str(e)}",var_value
            )
        except ValueError :
            self.interpreter.raise_error(
                TypeError,
                f"Invalid value for parsing as {var_type}: '{var_value}'",
                var_value,
            )
    def check_correct_var_name(self, var_name: str):
        if var_name[0].isdigit():
            self.interpreter.raise_error(
                VariableError, "Invalid variable name", var_name[0]
            )
        if ' ' in var_name:
            self.interpreter.raise_error(
                VariableError, "Variable names cannot contain spaces", var_name
                )

    def collection_assignment(self, collection_str: str, collection_type):
        elements = collection_str.strip("[]()").split(",")
        new_collection = []
        for element in elements:
            element = element.strip()
            if element != "":
                new_collection.append(self.variable_assignment(var_value=element))
        self.interpreter.log(
            "Collection Assignment", f"Assigned {new_collection} to collection"
        )
        return collection_type(new_collection)
