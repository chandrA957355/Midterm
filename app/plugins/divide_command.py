from decimal import Decimal, DivisionByZero

class DivideCommand:
    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        if num2 == 0:
            raise DivisionByZero("Division by zero is not allowed.")
        return num1 / num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        try:
            result = self.execute(num1, num2)
            result_queue.put(result)
        except DivisionByZero as e:
            result_queue.put(e)
