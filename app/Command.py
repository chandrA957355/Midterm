from decimal import Decimal
from abc import ABC, abstractmethod

class Command(ABC):
    operation_name: str

    @abstractmethod
    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        pass

    @abstractmethod
    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        pass
