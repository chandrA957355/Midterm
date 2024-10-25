# app/plugins/square_command.py
"""
This module defines the `SquareCommand` class for performing square operations.
"""

from decimal import Decimal
from app.command import Command

class SquareCommand(Command):
    """
    Command class for performing square operations.
    Implements the `execute` and `execute_multiprocessing` methods.
    """
    operation_name = "square"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Returns the square of the given number.

        Args:
            num1 (Decimal): The number to square.
            num2 (Decimal): Not used in this operation.

        Returns:
            Decimal: The square of num1.
        """
        return num1 * num1

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Performs the square operation using multiprocessing
        and puts the result into a queue.

        Args:
            num1 (Decimal): The number to square.
            num2 (Decimal): Not used in this operation.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        result = self.execute(num1, num2)
        result_queue.put(result)
