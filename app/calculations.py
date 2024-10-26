# app/calculations.py
"""
This module provides a Calculations class that manages arithmetic operation history 
using the PandasFacade for DataFrame operations. It supports adding, clearing, 
retrieving, filtering, saving, loading, and deleting calculation records.
"""

import pandas as pd
from app.calculation import Calculation
from app.pandas_facade import PandasFacade

class Calculations:
    """
    A class to manage calculations using the PandasFacade for DataFrame operations.
    """

    facade = PandasFacade()

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        """
        Add a new Calculation instance to the history.

        Args:
            calculation (Calculation): The calculation instance to add.
        """
        new_record = {
            "operation": calculation.operation.operation_name,
            "num1": calculation.a,
            "num2": calculation.b,
            "result": calculation.result
        }
        cls.facade.add_record(new_record)

    @classmethod
    def clear_history(cls):
        """
        Clear the entire history of calculations.
        """
        cls.facade.clear()

    @classmethod
    def get_all_calculations(cls) -> pd.DataFrame:
        """
        Retrieve all Calculation instances in the history.

        Returns:
            pd.DataFrame: A DataFrame containing all calculation records.
        """
        return cls.facade.dataframe

    @classmethod
    def filter_with_operation(cls, operation: str) -> pd.DataFrame:
        """
        Filter Calculation instances based on the specified operation.

        Args:
            operation (str): The name of the operation to filter by.

        Returns:
            pd.DataFrame: A DataFrame containing filtered calculation records.
        """
        return cls.facade.filter_by_operation(operation)

    @classmethod
    def save_history(cls, filepath: str):
        """
        Save the calculation history to a CSV file.

        Args:
            filepath (str): The path where the history should be saved.
        """
        cls.facade.save_to_file(filepath)

    @classmethod
    def load_history(cls, filepath: str):
        """
        Load calculation history from a CSV file.

        Args:
            filepath (str): The path from where the history should be loaded.
        """
        cls.facade.load_from_file(filepath)

    @classmethod
    def delete_history(cls, index: int):
        """
        Delete a specific calculation from the history by its index.

        Args:
            index (int): The index of the calculation to delete.
        """
        cls.facade.delete_record(index)
