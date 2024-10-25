from decimal import Decimal

class SquareCommand:
    operation_name = "square"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 * num1

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        result = self.execute(num1, num2)
        result_queue.put(result)
