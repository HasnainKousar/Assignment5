##########################
# Input Validation class
##########################


"""
This module provides input validation mechanisms for the calculator application.

Key functionalities include:
- Input Validation: Ensures that inputs meets required formats and constraints.
- Exception Handling: Raises custom validation errors when inputs are invalid.

"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


@dataclass
class InputValidator:
    """
    Validates and sanitizes Calculator inputs.
    
    """

    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """
        Validate and convert input to Decimal.
        
        Args:
            value (Any): The input value to validate.
            config (CalculatorConfig): The configuration object for validation rules.
        
        Returns:
            Decimal: The validated and converted number.
        
        Raises:
            ValidationError: If the input is invalid or exceeds limits.
        """
        try:
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Input exceeds maximum allowed value: {config.max_input_value}")
            return number.normalize()
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e
        

    