"""
Arithmetic Operations Module

This module provides basic arithmetic operations: addition, 
subtraction, multiplication, and division. Each operation takes 
two inputs and returns the result. The division operation raises 
an error if an attempt is made to divide by zero.
"""

def add(a, b):
    """
    Add two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.
    """
    return a + b

def subtract(a, b):
    """
    Subtract one number from another.

    Args:
        a: The minuend.
        b: The subtrahend.

    Returns:
        The result of a - b.
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The product of a and b.
    """
    return a * b

def divide(a, b):
    """
    Divide one number by another.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The result of a / b.

    Raises:
        ValueError: If b is zero.
    """
    if b != 0:
        return a / b
    else:
        raise ValueError("Cannot divide by zero")