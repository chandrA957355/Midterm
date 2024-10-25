import pandas as pd 
from app.Calculation import Calculation
from app.Pandas_Facade import PandasFacade  

class Calculations:
    """
    A class to manage calculations using the PandasFacade for DataFrame operations.
    """

    facade = PandasFacade() 

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
        """
        return cls.facade.dataframe

    @classmethod
    def filter_with_operation(cls, operation: str) -> pd.DataFrame:
        """
        Filter Calculation instances based on the specified operation.
        """
        return cls.facade.filter_by_operation(operation)

    @classmethod
    def save_history(cls, filepath: str):
        """
        Save the calculation history to a CSV file.
        """
        cls.facade.save_to_file(filepath)

    @classmethod
    def load_history(cls, filepath: str):
        """
        Load calculation history from a CSV file.
        """
        cls.facade.load_from_file(filepath)

    @classmethod
    def delete_history(cls, index: int):
        """
        Delete a specific calculation from the history by its index.
        """
        cls.facade.delete_record(index)
