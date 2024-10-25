# tests/test_calculations.py
import pytest
from decimal import Decimal
from app.Calculation import Calculation
from app.Calculations import Calculations
from app.plugins.add_command import AddCommand
from app.plugins.subtract_command import SubtractCommand
from app.plugins.multiply_command import MultiplyCommand
from app.plugins.divide_command import DivideCommand

@pytest.fixture
def setup_calculations():
    # Clear any existing history before each test
    Calculations.clear_history()

def test_add_calculation(setup_calculations):
    add_command = AddCommand()
    calculation = Calculation(Decimal(2), Decimal(3), add_command)
    calculation.operate()
    Calculations.add_calculation(calculation)
    
    # Verify the calculation is added to history
    history = Calculations.get_all_calculations()
    assert len(history) == 1
    assert history.iloc[0]["result"] == Decimal(5)

def test_clear_history(setup_calculations):
    add_command = AddCommand()
    calculation = Calculation(Decimal(2), Decimal(3), add_command)
    calculation.operate()
    Calculations.add_calculation(calculation)
    
    # Clear history
    Calculations.clear_history()
    history = Calculations.get_all_calculations()
    assert history.empty

def test_filter_with_operation(setup_calculations):
    add_command = AddCommand()
    subtract_command = SubtractCommand()
    
    calculation1 = Calculation(Decimal(2), Decimal(3), add_command)
    calculation1.operate()
    Calculations.add_calculation(calculation1)
    
    calculation2 = Calculation(Decimal(5), Decimal(3), subtract_command)
    calculation2.operate()
    Calculations.add_calculation(calculation2)
    
    # Filter by "add" operation
    filtered = Calculations.filter_with_operation("add")
    assert len(filtered) == 1
    assert filtered.iloc[0]["operation"] == "add"

def test_save_and_load_history(setup_calculations, tmp_path):
    add_command = AddCommand()
    calculation = Calculation(Decimal(2), Decimal(3), add_command)
    calculation.operate()
    Calculations.add_calculation(calculation)
    
    # Save history
    file_path = tmp_path / "history.csv"
    Calculations.save_history(str(file_path))
    
    # Clear history and verify it's empty
    Calculations.clear_history()
    assert Calculations.get_all_calculations().empty
    
    # Load history from the file and verify
    Calculations.load_history(str(file_path))
    history = Calculations.get_all_calculations()
    assert len(history) == 1
    assert history.iloc[0]["result"] == Decimal(5)

def test_delete_history(setup_calculations):
    add_command = AddCommand()
    calculation = Calculation(Decimal(2), Decimal(3), add_command)
    calculation.operate()
    Calculations.add_calculation(calculation)
    
    # Delete the calculation
    Calculations.delete_history(0)
    history = Calculations.get_all_calculations()
    assert history.empty

def test_delete_invalid_index(setup_calculations, capsys):
    add_command = AddCommand()
    calculation = Calculation(Decimal(2), Decimal(3), add_command)
    calculation.operate()
    Calculations.add_calculation(calculation)
    
    # Try deleting an invalid index
    Calculations.delete_history(10)
    captured = capsys.readouterr()
    assert "Index 10 is out of range. Unable to delete." in captured.out

def test_get_all_calculations_empty(setup_calculations):
    # Verify history is empty
    history = Calculations.get_all_calculations()
    assert history.empty
