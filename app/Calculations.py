import pandas as pd
from app.Calculation import Calculation
from decimal import Decimal
from typing import List, Optional

class Calculations:
    """
    A class to manage a history of calculations using Pandas.

    Attributes:
        history (pd.DataFrame): A DataFrame to store calculation instances.

    Methods:
        add_calculation(calculation: Calculation):
            Adds a new Calculation instance to the history.
        
        clear_history():
            Clears the entire history of calculations.
        
        get_latest() -> Optional[Calculation]:
            Returns the most recent Calculation instance, or None if the history is empty.
        
        get_all_calculations() -> List[Calculation]:
            Returns all Calculation instances in the history.
        
        filter_with_operation(operation: str) -> List[Calculation]:
            Returns a list of Calculation instances that match the specified operation.
        
        save_history(filepath: str):
            Saves the calculation history to a CSV file.
        
        load_history(filepath: str):
            Loads calculation history from a CSV file.
    """

    history = pd.DataFrame(columns=["operation", "num1", "num2", "result"])

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        """
        Add a new Calculation instance to the history.

        Args:
            calculation (Calculation): The Calculation instance to add.
        """
        new_record = {
            "operation": calculation.operation.__name__,
            "num1": calculation.num1,
            "num2": calculation.num2,
            "result": calculation.result
        }
        cls.history = cls.history.append(new_record, ignore_index=True)
    
    @classmethod
    def clear_history(cls):
        """
        Clear the entire history of calculations.
        """
        cls.history = pd.DataFrame(columns=["operation", "num1", "num2", "result"])
        
    @classmethod
    def get_latest(cls) -> Optional[Calculation]:
        """
        Retrieve the most recent Calculation instance.

        Returns:
            Optional[Calculation]: The latest Calculation instance, or None if the history is empty.
        """
        if not cls.history.empty:
            latest = cls.history.iloc[-1]
            return Calculation(latest["operation"], Decimal(latest["num1"]), Decimal(latest["num2"]), Decimal(latest["result"]))
        return None
    
    @classmethod
    def get_all_calculations(cls) -> pd.DataFrame:
        """
        Retrieve all Calculation instances in the history.

        Returns:
            pd.DataFrame: A DataFrame of all Calculation instances.
        """
        return cls.history

    @classmethod
    def filter_with_operation(cls, operation: str) -> pd.DataFrame:
        """
        Filter Calculation instances based on the specified operation.

        Args:
            operation (str): The name of the operation to filter by.

        Returns:
            pd.DataFrame: A DataFrame of Calculation instances that match the operation.
        """
        return cls.history[cls.history["operation"] == operation]

    @classmethod
    def save_history(cls, filepath: str):
        """
        Save the calculation history to a CSV file.

        Args:
            filepath (str): The path to the file where history will be saved.
        """
        cls.history.to_csv(filepath, index=False)
    
    @classmethod
    def load_history(cls, filepath: str):
        """
        Load calculation history from a CSV file.

        Args:
            filepath (str): The path to the CSV file to load.
        """
        cls.history = pd.read_csv(filepath)
