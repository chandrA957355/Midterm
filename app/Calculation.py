from decimal import Decimal

class Calculation:
    """
    A class representing a mathematical calculation.
    """
    
    def __init__(self, a: Decimal, b: Decimal, operation):
        """
        Initialize a Calculation instance.
        """
        self.a = a
        self.b = b
        self.operation = operation
        self.result = None

    def operate(self) -> Decimal:
        """
        Perform the arithmetic operation on the operands.
        """
        self.result = self.operation.execute(self.a, self.b)
        return self.result

    def __str__(self) -> str:
        """
        Return a string representation of the Calculation instance.
        """
        return f"Calculation({self.a}, {self.b}, {self.operation.operation_name})"
