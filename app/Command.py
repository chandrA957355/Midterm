# app/command.py
"""
This module defines the abstract base class `Command` for executing arithmetic operations.
"""

from decimal import Decimal
from abc import ABC, abstractmethod

class Command(ABC):
    """
    Abstract base class for arithmetic operations. 
    Provides a common interface for executing operations.
    """
    operation_name: str

    @abstractmethod
    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        """
        Execute the operation on two Decimal numbers.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.

        Returns:
            Decimal: The result of the operation.
        """
        # No implementation needed for abstract methods

    @abstractmethod
    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        """
        Execute the operation using multiprocessing and store the result in a queue.

        Args:
            num1 (Decimal): The first number.
            num2 (Decimal): The second number.
            result_queue (multiprocessing.Queue): Queue to store the result.
        """
        # No implementation needed for abstract methods
