# Tests for the operations module


import pytest
from decimal import Decimal
from typing import Any, Dict, Type


from app.exceptions import ValidationError

from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    OperationFactory,
)


class TestOperation:
    """ Test base Operation class functionality. """

    def test_str_representation(self):
        """ Test string representation of the Operation class. """
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a
            
        assert str(TestOp()) == "TestOp" # str representation should be the class name


class BaseOperationTest:
    """ A base operation for testing purposes. """
    
    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Any]
    invalid_test_cases: Dict[str, Any]

    def test_valid_operations(self):

        """test operation with valid operands"""

        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            expected = Decimal(str(case['expected']))
            result = operation.execute(a, b)
            assert result == expected, f'Failed case: {name}'

    def test_invalid_operations(self):
        """test operation with invalid operands"""

        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case['a']))
            b = Decimal(str(case['b']))
            error = case.get('error', ValidationError)
            error_message = case.get('message', "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)

    
class TestAddition(BaseOperationTest):
    """ Test Addition operation. """

    operation_class = Addition
    valid_test_cases = {
        "positive_integers": {"a": 1, "b": 2, "expected": 3},
        "negative_integers": {"a": -1, "b": -2, "expected": -3},
        "mixed_integers": {"a": 1, "b": -2, "expected": -1},
        "decimal_numbers": {"a": 1.5, "b": 2.5, "expected": 4.0},
        "zero": {"a": 0, "b": 0, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 2e10, "expected": 3e10},
    }
    invalid_test_cases = {} #addition does not have invalid cases


class TestSubtraction(BaseOperationTest):
    """ Test Subtraction operation. """

    operation_class = Subtraction
    valid_test_cases = {
        "positive_integers": {"a": 5, "b": 3, "expected": 2},
        "negative_integers": {"a": -5, "b": -3, "expected": -2},
        "mixed_integers": {"a": 1, "b": -2, "expected": 3},
        "decimal_numbers": {"a": 5.5, "b": 2.5, "expected": 3.0},
        "zero": {"a": 0, "b": 0, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 2e10, "expected": -1e10},
    }
    invalid_test_cases = {} #subtraction does not have invalid cases


class TestMultiplication(BaseOperationTest):
    """ Test Multiplication operation. """

    operation_class = Multiplication
    valid_test_cases = {
        "positive_integers": {"a": 2, "b": 3, "expected": 6},
        "negative_integers": {"a": -2, "b": -3, "expected": 6},
        "mixed_integers": {"a": 2, "b": -3, "expected": -6},
        "decimal_numbers": {"a": 1.5, "b": 2.0, "expected": 3.0},
        "zero": {"a": 0, "b": 5, "expected": 0},
        "large_numbers": {"a": 1e10, "b": 2e10, "expected": 2e20},
    }
    invalid_test_cases = {} #multiplication does not have invalid cases

class TestDivision(BaseOperationTest):
    """ Test Division operation. """

    operation_class = Division
    valid_test_cases = {
        "positive_integers": {"a": 6, "b": 3, "expected": 2},
        "negative_integers": {"a": -6, "b": -3, "expected": 2},
        "mixed_integers": {"a": 6, "b": -3, "expected": -2},
        "decimal_numbers": {"a": 7.5, "b": 2.5, "expected": 3.0},
        "zero_numerator": {"a": 0, "b": 5, "expected": 0},
        "large_numbers": {"a": 1e20, "b": 1e10, "expected": 1e10},
    }
    invalid_test_cases = {
        "zero_denominator": {
            "a": 5,
            "b": 0,
            "error": ValidationError,
            "message": "Division by zero is not allowed"
        },
    }

class TestPower(BaseOperationTest):
    """ Test Power operation. """

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": 2, "b": 3, "expected": 8},
        "zero_exponent": {"a": 5, "b": 0, "expected": 1},
        "one_exponent": {"a": 5, "b": 1, "expected": 5},
        "decimal_base": {"a": 2.5, "b": 2, "expected": 6.25},
        "zero_base": {"a": 0, "b": 5, "expected": 0},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": 2,
            "b": -3,
            "error": ValidationError,
            "message": "Exponent must be non-negative."
        },
        
    }

class TestRoot(BaseOperationTest):
    """ Test Root operation. """

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": 4, "b": 2, "expected": 2},
        "cube_root": {"a": 27, "b": 3, "expected": 3},
        "fourth_root": {"a": 16, "b": 4, "expected": 2},
        "decimal_base": {"a": 2.25, "b": 2, "expected": 1.5},
    }

    invalid_test_cases = {
        "negative_base": {
            "a": -4,
            "b": 2,
            "error": ValidationError,
            "message": "cannot calculate root of a negative number."
        },
        "zero_root": {
            "a": 4,
            "b": 0,
            "error": ValidationError,
            "message": "Zero root is not defined."
        },
    }


    