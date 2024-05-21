

from exceptions import OperationError
from type.interpreter_type import InterpreterType


class OperationManager:
    def __init__(self, interpreter: InterpreterType):
        self.interpreter = interpreter

    def arithmetic_operation(self, expression):
        try:
            result = self.interpreter.parser.safe_eval(expression, self.interpreter.var_manager.vars)
        except SyntaxError:
            self.interpreter.raise_error(OperationError, "Invalid expression", expression)
        return result

    def perform_operation(self, var_name, var_value, operator):
        current_value = self.interpreter.var_manager.vars[var_name]
        operation_value = self.arithmetic_operation(var_value)
        if operator == "+=":
            result = current_value + operation_value
        elif operator == "-=":
            result = current_value - operation_value
        elif operator == "*=":
            result = current_value * operation_value
        elif operator == "/=":
            result = current_value / operation_value
        elif operator == "%=":
            result = current_value % operation_value
        else:
            self.interpreter.raise_error(OperationError, "Invalid operator", operator)
        self.interpreter.log(
            "Arithmetic Operation",
            f"{operator} operation: {var_name} updated to {result}",
        )
        return result
