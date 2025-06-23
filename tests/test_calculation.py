# Test for the calculation module

import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


def test_addition():
    calc = Calculation(operation="Addition", operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('8.0')


def test_subtraction():
    calc = Calculation(operation="Subtraction", operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_multiplication():
    calc = Calculation(operation="Multiplication", operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('15.0')

def test_division():
    calc = Calculation(operation="Division", operand1=Decimal('6.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed."):
        Calculation(operation="Division", operand1=Decimal('6.0'), operand2=Decimal('0.0'))

def test_power():
    calc = Calculation(operation="Power", operand1=Decimal('2.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('8.0')

def test_negative_power():
    with pytest.raises(OperationError, match="Exponent must be non-negative."):
        Calculation(operation="Power", operand1=Decimal('2.0'), operand2=Decimal('-3.0'))

def test_root():
    calc = Calculation(operation="Root", operand1=Decimal('8.0'), operand2=Decimal('3.0'))
    assert calc.result == Decimal('2.0')

def test_invalid_root():
    with pytest.raises(OperationError, match="cannot calculate root of a negative number."):
        Calculation(operation="Root", operand1=Decimal('-8.0'), operand2=Decimal('3.0'))

def test_zero_root():
    with pytest.raises(OperationError, match="Zero root is not defined."):
        Calculation(operation="Root", operand1=Decimal('8.0'), operand2=Decimal('0.0'))


def test_invalid_operation():
    with pytest.raises(OperationError, match="Unknown operation: InvalidOperation"):
        Calculation(operation="InvalidOperation", operand1=Decimal('5.0'), operand2=Decimal('3.0'))


def test_to_dict():
    calc = Calculation(operation="Addition", operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Addition",
        "operand1": "5.0",
        "operand2": "3.0",
        "result": "8.0",
        "timestamp": calc.timestamp.isoformat()
    }

def test_from_dict():
    data = {
        "operation": "Subtraction",
        "operand1": "10.0",
        "operand2": "4.0",
        "result": "6.0",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Subtraction"
    assert calc.operand1 == Decimal('10.0')
    assert calc.operand2 == Decimal('4.0')
    assert calc.result == Decimal('6.0')
  


def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "invalid",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)




def test_format_result():
    calc = Calculation(operation="Division", operand1=Decimal('1'), operand2=Decimal('3'))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"



def test_equality():
    calc1 = Calculation(operation="Addition", operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    calc2 = Calculation(operation="Addition", operand1=Decimal('5.0'), operand2=Decimal('3.0'))
    calc3 = Calculation(operation="Subtraction", operand1=Decimal('5.0'), operand2=Decimal('3.0'))

    assert calc1 == calc2
    assert calc1 != calc3


def test_from_dict_result_mismatch(caplog):
    #arrange
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "6",  # Incorrect result to trigger logging.warning
        "timestamp": datetime.now().isoformat()
    }

    #act
    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    # Assert
    assert "Loaded calculation result 6 differs from computed result 5" in caplog.text


def test_calculation_failed_exception():
    """Test that calculation failures are properly handled with OperationError."""
    # This test aims to trigger the exception handling on line 81 of calculation.py
    # by creating a scenario that causes an InvalidOperation, ValueError, or ArithmeticError
    
    # Test with extremely large numbers that could cause overflow/calculation errors
    with pytest.raises(OperationError, match="Calculation Failed"):
        # Using very large Decimal numbers that might cause issues in pow() conversion
        calc = Calculation(
            operation="Power", 
            operand1=Decimal('1e308'), 
            operand2=Decimal('1e308')
        )

