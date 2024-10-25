import pandas as pd
from app.Calculation import Calculation
from decimal import Decimal

class Calculations:
    """
    A facade class to manage a history of calculations using Pandas.
    """

    history = pd.DataFrame(columns=["operation", "num1", "num2", "result"])

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        """
        Add a new Calculation instance to the history.
        """
        new_record = {
            "operation": calculation.operation.operation_name,
            "num1": calculation.a,
            "num2": calculation.b,
            "result": calculation.result
        }
        cls.history = pd.concat([cls.history, pd.DataFrame([new_record])], ignore_index=True)
    
    @classmethod
    def clear_history(cls):
        """
        Clear the entire history of calculations.
        """
        cls.history = pd.DataFrame(columns=["operation", "num1", "num2", "result"])
    
    @classmethod
    def get_all_calculations(cls) -> pd.DataFrame:
        """
        Retrieve all Calculation instances in the history.
        """
        return cls.history

    @classmethod
    def filter_with_operation(cls, operation: str) -> pd.DataFrame:
        """
        Filter Calculation instances based on the specified operation.
        """
        return cls.history[cls.history["operation"] == operation]

    @classmethod
    def save_history(cls, filepath: str):
        """
        Save the calculation history to a CSV file.
        """
        cls.history.to_csv(filepath, index=False)
    
    @classmethod
    def load_history(cls, filepath: str):
        """
        Load calculation history from a CSV file.
        """
        cls.history = pd.read_csv(filepath)

    @classmethod
    def delete_history(cls, index: int):
        """
        Delete a specific calculation from the history by its index.

        Args:
            index (int): The index of the calculation to delete.
        """
        if 0 <= index < len(cls.history):
            cls.history = cls.history.drop(index).reset_index(drop=True)
            print(f"Deleted calculation at index {index}.")
        else:
            print(f"Index {index} is out of range. Unable to delete.")