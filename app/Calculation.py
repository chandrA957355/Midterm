"""
Calculation Class

The Calculation class, that encapsulates the concept of a mathematical calculation
integrating two Decimal numbers and an initialized arithmetic operation which is
defined in this module. Methods for performing the process and generating calculation
instances are provided in the class.
"""

from decimal import Decimal
from typing import Callable
from app.Operations import add, subtract, multiply, divide

class Calculation:
    """
    A class representing a mathematical calculation.

    Attributes:
        a (Decimal): The first operand in the calculation.
        b (Decimal): The second operand in the calculation.
        operation (Callable[[Decimal, Decimal], Decimal]): The operation to perform.

    Methods:
        operate() -> Decimal:
            Executes the operation on the operands and returns the result.
        
        create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> 'Calculation':
            Static method to create a new Calculation instance.
        
        __strrepr__() -> str:
            Returns a string representation of the Calculation instance.
    """
    
    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """
        Initialize a Calculation instance.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.
            operation (Callable[[Decimal, Decimal], Decimal]): The operation to perform.
        """
        self.a = a
        self.b = b
        self.operation = operation

    def operate(self) -> Decimal:
        """
        Perform the arithmetic operation on the operands.

        Returns:
            Decimal: The result of the operation.
        """
        return self.operation(self.a, self.b)

    @staticmethod
    def create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> 'Calculation':
        """
        Create a new Calculation instance.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.
            operation (Callable[[Decimal, Decimal], Decimal]): The operation to perform.

        Returns:
            Calculation: A new instance of Calculation.
        """
        return Calculation(a, b, operation)
    
    def __strrepr__(self) -> str:
        """
        Return a string representation of the Calculation instance.

        Returns:
            str: A string representing the Calculation.
        """
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"