# Tests for the calculator module

import datetime
import logging
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import run_calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

# Fixture to create a temporary directory for testing
@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        #patch properties to use the temporary directory
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            # Set the mock return values to the temporary directory
            mock_log_dir.return_value = temp_path / 'logs'
            mock_log_file.return_value = temp_path / 'logs' / 'calculator.log'
            mock_history_dir.return_value = temp_path / 'history'
            mock_history_file.return_value = temp_path / 'history' / 'calculator_history.csv'

            # Return a Calculator instance with the mocked config
            yield Calculator(config=config)

# Test for the Calculator class initialization

def test_calculator_initialization(calculator):
    """Test that the Calculator class initializes correctly with the provided configuration."""
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None


# Test Logging setup

@patch('app.calculator.logging.info')
def test_logging_setup(mock_logging_info):
    """ Test that the logging is set up correctly in the Calculator class."""
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        
        mock_log_dir.return_value = Path('./test_logs')
        mock_log_file.return_value = Path('./test_logs/calculator.log')

        calculator = Calculator(CalculatorConfig())
        mock_logging_info.assert_any_call("Calculator initialized with configuration")


# Test adding and removing observers

def test_add_observer(calculator):
    """Test that an observer can be added to the Calculator instance."""
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    """Test that an observer can be removed from the Calculator instance."""
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers


# Test Setting Operation

def test_set_operation(calculator):
    """Test that the operation strategy can be set correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation


#Test Performing Operations
def test_perform_operation_addition(calculator):
    """Test that performing an operation works correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)

    result = calculator.perform_calculation(Decimal('5'), Decimal('3'))
    assert result == Decimal('8')

def test_perform_operatio_validation_error(calculator):
    """Test that performing an operation raises a ValidationError for invalid input."""
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_calculation('invalid', Decimal('3'))

def test_perform_operation_operation_error(calculator):
    """Test that performing an operation without setting an operation raises OperationError."""
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_calculation(Decimal('5'), Decimal('3'))



 