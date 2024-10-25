from decimal import Decimal
from app.Command import Command

class SubtractCommand(Command):
    operation_name = "subtract"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 - num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        result = self.execute(num1, num2)
        result_queue.put(result)
