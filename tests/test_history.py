# Tests for the history module

import logging
import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig



# Sample set up for mock calculation
calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "addition"
calculation_mock.operand1 = "5"
calculation_mock.operand2 = "4"
calculation_mock.result = "9"

# Test cases for LoggingObserver

@patch('logging.info')
def test_logging_observer_logs_calculation(logging_info_mock):
    """Test that LoggingObserver logs the calculation correctly."""
    observer = LoggingObserver()
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with(
        "Calculation performed: addition (5, 4) = 9"
    )

def test_logging_observer_no_calculation():
    """Test that LoggingObserver does not log if no calculation is provided."""
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)


# Test cases for AutoSaveObserver

def test_autosave_observer_triggers_save():
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = CalculatorConfig()
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)

    observer.update(calculation_mock)
    calculator_mock.save_history.assert_called_once()


@patch('logging.info')
def test_autosave_observer_does_not_trigger_save_when_auto_save_disabled(logging_info_mock):
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = CalculatorConfig()
    calculator_mock.config.auto_save = False
    observer = AutoSaveObserver(calculator_mock)

    observer.update(calculation_mock)
    calculator_mock.save_history.assert_not_called()
    logging_info_mock.assert_not_called()

# additional negative test case for AutoSaveObserver

def test_autosave_observer_invalid_calculator():
    """Test that AutoSaveObserver raises TypeError if calculator is invalid."""
    with pytest.raises(TypeError):
        AutoSaveObserver(calculator=None)


def test_autosave_observer_no_calculation():
    """Test that AutoSaveObserver does not save if no calculation is provided."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)

    with pytest.raises(AttributeError):
        observer.update(None)

