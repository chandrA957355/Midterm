import pytest
from decimal import Decimal, DivisionByZero
from app.plugins.add_command import AddCommand
from app.plugins.subtract_command import SubtractCommand
from app.plugins.multiply_command import MultiplyCommand
from app.plugins.divide_command import DivideCommand
from multiprocessing import Queue

def test_add_command():
    command = AddCommand()
    result = command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(5)

def test_add_command_multiprocessing():
    command = AddCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(5)

def test_subtract_command():
    command = SubtractCommand()
    result = command.execute(Decimal(5), Decimal(3))
    assert result == Decimal(2)

def test_subtract_command_multiprocessing():
    command = SubtractCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(5), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

def test_multiply_command():
    command = MultiplyCommand()
    result = command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(6)

def test_multiply_command_multiprocessing():
    command = MultiplyCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(6)

def test_divide_command():
    command = DivideCommand()
    result = command.execute(Decimal(6), Decimal(3))
    assert result == Decimal(2)

def test_divide_command_multiprocessing():
    command = DivideCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(6), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

def test_divide_by_zero():
    command = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        command.execute(Decimal(6), Decimal(0))

def test_divide_command_execute():
    divide_command = DivideCommand()

    # Test normal division
    assert divide_command.execute(Decimal(6), Decimal(3)) == Decimal(2)
    assert divide_command.execute(Decimal(-6), Decimal(3)) == Decimal(-2)
    assert divide_command.execute(Decimal(0), Decimal(3)) == Decimal(0)

    # Test division by zero
    with pytest.raises(DivisionByZero, match="Division by zero is not allowed."):
        divide_command.execute(Decimal(6), Decimal(0))

def test_divide_command_execute_multiprocessing():
    divide_command = DivideCommand()
    result_queue = Queue()

    # Test normal division using multiprocessing
    divide_command.execute_multiprocessing(Decimal(6), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

    # Test division by zero using multiprocessing
    divide_command.execute_multiprocessing(Decimal(6), Decimal(0), result_queue)
    result = result_queue.get()
    assert isinstance(result, DivisionByZero)
    assert str(result) == "Division by zero is not allowed."