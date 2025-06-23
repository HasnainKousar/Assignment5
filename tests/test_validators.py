# Tests for the validators module

from logging import config
import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

# sample configuration with a max input value of 100,000 for testing purposes
config = CalculatorConfig(max_input_value=Decimal('100000'))


def test_validate_number_positive_integer():
    """Test validation of a positive integer."""
    assert InputValidator.validate_number(123, config) == Decimal('123')


def test_validate_number_postive_decimal():
    """Test validation of a positive decimal."""
    assert InputValidator.validate_number(123.456, config) == Decimal('123.456').normalize()

def test_validate_number_positive_string():
    """Test validation of a positive number in string format."""
    assert InputValidator.validate_number("123", config) == Decimal('123')

def test_validate_number_positive_string_decimal():
    """Test validation of a positive decimal in string format."""
    assert InputValidator.validate_number("123.456", config) == Decimal('123.456').normalize()

def test_validate_number_negative_integer():
    """Test validation of a negative integer."""
    assert InputValidator.validate_number(-123, config) == Decimal('-123')

def test_validate_number_negative_decimal():
    """Test validation of a negative decimal."""
    assert InputValidator.validate_number(-123.456, config) == Decimal('-123.456').normalize()

def test_validate_number_negative_string():
    """Test validation of a negative number in string format."""
    assert InputValidator.validate_number("-123", config) == Decimal('-123')

def test_validate_number_negative_string_decimal():
    """Test validation of a negative decimal in string format."""
    assert InputValidator.validate_number("-123.456", config) == Decimal('-123.456').normalize()


def test_validate_number_zero():
    """Test validation of zero."""
    assert InputValidator.validate_number(0, config) == Decimal('0')

def test_validate_number_trimmed_string():
    """Test validation of a number in a string with leading/trailing spaces."""
    assert InputValidator.validate_number("  123.456  ", config) == Decimal('123.456').normalize()


# Negative test cases

def test_validate_number_invalid_string():
    """Test validation of an invalid string."""
    with pytest.raises(ValidationError, match="Invalid number format: abc"):
        InputValidator.validate_number("abc", config)

def test_validate_number_exceeds_max_value():
    """Test validation of a number that exceeds the maximum allowed value."""
    with pytest.raises(ValidationError, match="Input exceeds maximum allowed value: 100000"):
        InputValidator.validate_number(Decimal('100001'), config)

def test_validate_number_exceeds_max_value_string():
    """Test validation of a string that exceeds the maximum allowed value."""
    with pytest.raises(ValidationError, match="Input exceeds maximum allowed value: 100000"):
        InputValidator.validate_number("100001", config)


def test_validate_number_empty_string():
    """Test validation of an empty string."""
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_number("", config)


def test_validate_number_none_value():
    """Test validation of a None value."""
    with pytest.raises(ValidationError, match="Invalid number format: None"):
        InputValidator.validate_number(None, config)

