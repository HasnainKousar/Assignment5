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

@patch('app.calculator.logging.warning')
@patch('app.calculator.logging.info')
def test_calculator_init_load_history_failure(mock_logging_info, mock_logging_warning):
    """Test calculator initialization when load_history fails."""
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        
        mock_log_dir.return_value = Path('./test_logs')
        mock_log_file.return_value = Path('./test_logs/calculator.log')
        
        # Mock load_history to raise an exception
        with patch.object(Calculator, 'load_history') as mock_load_history:
            mock_load_history.side_effect = Exception("Failed to load history")
            
            calculator = Calculator(CalculatorConfig())
            
            # Verify the warning was logged
            mock_logging_warning.assert_called_once_with("Could not load existing history: Failed to load history")
            # Verify initialization still completed successfully
            mock_logging_info.assert_any_call("Calculator initialized with configuration")

@patch('builtins.print')
def test_setup_logging_failure(mock_print):
    """Test _setup_logging method failure."""
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        
        mock_log_dir.return_value = Path('./test_logs')
        mock_log_file.return_value = Path('./test_logs/calculator.log')
        
        # Mock logging.basicConfig to raise an exception inside _setup_logging
        with patch('app.calculator.logging.basicConfig') as mock_basic_config:
            mock_basic_config.side_effect = Exception("Permission denied")
            
            with pytest.raises(Exception, match="Permission denied"):
                Calculator(CalculatorConfig())
            
            # Verify the error message was printed
            mock_print.assert_called_once_with("Error setting up logging: Permission denied")


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

@patch('app.calculator.logging.error')
def test_perform_calculation_general_exception(mock_logging_error, calculator):
    """Test that general exceptions in perform_calculation are handled correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    
    # Mock the operation strategy to raise a general exception
    with patch.object(calculator.operation_strategy, 'execute') as mock_execute:
        mock_execute.side_effect = Exception("Calculation failed")
        
        with pytest.raises(OperationError, match="Operation failed: Calculation failed"):
            calculator.perform_calculation(Decimal('5'), Decimal('3'))
        
        # Verify the error was logged
        mock_logging_error.assert_called_once_with("Operation failed: Calculation failed")


# Test undo and redo functionality

def test_undo(calculator):
    """Test that undoing an operation works correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_calculation(4,5)
    calculator.undo()
    assert len(calculator.history) == 0

def test_redo(calculator):
    """Test that redoing an operation works correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_calculation(4,5)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1


# Test for history management

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    """Test that the history is saved correctly to a CSV file."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_calculation(4, 5)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    #Mock CSV data to match the expected format in from_dict
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['Addition'],  # Use correct operation name
        'operand1': [4],
        'operand2': [5],
        'result': [9],
        'timestamp': [datetime.datetime.now().isoformat()]
    })

    # Test loading history from a CSV file
    try:
        calculator.load_history()
        #verify history length
        assert len(calculator.history) == 1
        assert calculator.history[0].operation == 'Addition'
        assert calculator.history[0].operand1 == Decimal('4')
        assert calculator.history[0].operand2 == Decimal('5')
        assert calculator.history[0].result == Decimal('9')
    except OperationError:
        pytest.fail("Loading history raised an OperationError unexpectedly.")


def test_clear_history(calculator):
    """Test that clearing the history works correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_calculation(4, 5)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []



# Test running the REPL


#test running the REPL with valid commands
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_run_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        run_calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Exiting the calculator REPL. Goodbye!")

# Test running the REPL with an error in save_history
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_run_calculator_repl_exit_save_error(mock_print, mock_input):
    """Test REPL exit when save_history fails due to an exception."""
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        # Make save_history raise an exception
        mock_save_history.side_effect = Exception("Save failed")
        
        run_calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("Warning: Could not save history before exiting: Save failed")
        mock_print.assert_any_call("Exiting the calculator REPL. Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_run_calculator_repl_help(mock_print, mock_input):
    """Test REPL help command."""
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        run_calculator_repl()
        mock_save_history.assert_called_once()  # save_history is called during exit
        mock_print.assert_any_call("\nAvailable commands:")
        mock_print.assert_any_call("  add, subtract, multiply, divide, power, root - Perform arithmetic operations")
        mock_print.assert_any_call("  exit - Exit the calculator REPL")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    run_calculator_repl()
    mock_print.assert_any_call("\nResult: 5")

@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_history_empty(mock_calculator_class, mock_print, mock_input):
    """Test REPL history command with empty history (lines 72-74)."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.show_history.return_value = []  # Empty history
    mock_calc.add_observer = Mock()
    mock_calculator_class.return_value = mock_calc
    
    run_calculator_repl()
    
    # Verify save_history was called on exit
    mock_calc.save_history.assert_called()
    # Verify the correct message for empty history
    mock_print.assert_any_call("No calculations in history.")

@patch('builtins.input', side_effect=['add', '2', '3', 'multiply', '4', '5', 'history', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_history_with_calculations(mock_calculator_class, mock_print, mock_input):
    """Test REPL history command with calculations in history (lines 72, 75-77)."""
    # Create a mock calculator instance
    mock_calc = Mock()
    # Mock the show_history to return some calculations when called
    mock_calc.show_history.return_value = [
        "Addition(2, 3) = 5",
        "Multiplication(4, 5) = 20"
    ]
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    mock_calc.perform_calculation.side_effect = [5, 20]  # Return values for calculations
    mock_calculator_class.return_value = mock_calc
    
    run_calculator_repl()
    
    # Verify save_history was called on exit
    mock_calc.save_history.assert_called()
    # Verify the correct messages for history with calculations
    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1: Addition(2, 3) = 5")
    mock_print.assert_any_call("2: Multiplication(4, 5) = 20")

@patch('builtins.input', side_effect=['add', '2', '3', 'clear', 'exit'])
@patch('builtins.print')
@patch('app.calculator_repl.Calculator')
def test_run_calculator_repl_clear_history(mock_calculator_class, mock_print, mock_input):
    """Test REPL clear command."""
    # Create a mock calculator instance
    mock_calc = Mock()
    mock_calc.add_observer = Mock()
    mock_calc.set_operation = Mock()
    mock_calc.perform_calculation.return_value = 5
    mock_calc.clear_history = Mock()
    mock_calculator_class.return_value = mock_calc
    
    run_calculator_repl()
    
    # Verify save_history was called on exit
    mock_calc.save_history.assert_called()
    # Verify clear_history was called
    mock_calc.clear_history.assert_called_once()
    # Verify the correct message for clear
    mock_print.assert_any_call("History cleared.")

def test_max_history_size_exceeded(calculator):
    """Test that history is trimmed when max_history_size is exceeded."""
    # Set a small max_history_size for testing
    calculator.config.max_history_size = 2
    
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    
    # Perform calculations to exceed the max history size
    calculator.perform_calculation(1, 1)
    calculator.perform_calculation(2, 2)
    assert len(calculator.history) == 2
    
    # Perform one more calculation to exceed the limit
    calculator.perform_calculation(3, 3)  # This triggers line 247: history.pop(0)
    
    # Verify history is trimmed (oldest calculation removed)
    assert len(calculator.history) == 2
    assert calculator.history[0].operand1 == Decimal('2')  # First calculation removed
    assert calculator.history[1].operand1 == Decimal('3')

@patch('app.calculator.logging.error')
def test_save_history_exception(mock_logging_error, calculator):
    """Test that save_history handles exceptions correctly."""
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_calculation(4, 5)
    
    # Mock pd.DataFrame to raise an exception
    with patch('app.calculator.pd.DataFrame') as mock_dataframe:
        mock_dataframe.side_effect = Exception("DataFrame creation failed")
        
        with pytest.raises(OperationError, match="Failed to save history: DataFrame creation failed"):
            calculator.save_history()
        
        # Verify the error was logged
        mock_logging_error.assert_called_once_with("Failed to save history: DataFrame creation failed")

@patch('app.calculator.logging.info')
@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_empty_history(mock_to_csv, mock_logging_info, calculator):
    """Test that empty history is saved correctly (lines 297-300)."""
    # Ensure calculator has no history
    assert len(calculator.history) == 0
    
    calculator.save_history()
    
    # Verify empty DataFrame with headers was created and saved
    mock_to_csv.assert_called_once()
    # Verify the info message for empty history was logged
    mock_logging_info.assert_called_with(f"Empty history file created at {calculator.config.history_file}")

@patch('app.calculator.logging.error')
def test_load_history_exception(mock_logging_error, calculator):
    """Test that load_history handles exceptions correctly."""
    # Clear any existing history
    calculator.history.clear()
    
    # Mock pd.read_csv to raise an exception
    with patch('app.calculator.pd.read_csv') as mock_read_csv:
        mock_read_csv.side_effect = Exception("CSV read failed")
        
        # Mock pathlib.Path.exists to return True so we enter the try block
        with patch('pathlib.Path.exists', return_value=True):
            with pytest.raises(OperationError, match="Failed to load history: CSV read failed"):
                calculator.load_history()
            
            # Verify the error was logged
            mock_logging_error.assert_called_once_with("Failed to load history: CSV read failed")

def test_get_history_dataframe(calculator):
    """Test get_history_dataframe method."""
    # Add calculations to the history
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_calculation(2, 3)
    calculator.perform_calculation(4, 5)
    
    # Get the dataframe
    df = calculator.get_history_dataframe()
    
    # Verify the dataframe structure and content
    assert len(df) == 2
    assert list(df.columns) == ['operation', 'operand1', 'operand2', 'result', 'timestamp']
    assert df.iloc[0]['operation'] == 'Addition'
    assert df.iloc[0]['result'] == '5'
    assert df.iloc[1]['result'] == '9'

def test_get_history_dataframe_empty(calculator):
    """Test get_history_dataframe with empty history."""
    # Ensure history is empty
    calculator.history.clear()
    
    # Get the dataframe
    df = calculator.get_history_dataframe()
    
    # Verify empty dataframe
    assert len(df) == 0
    # When history_data is empty, pandas DataFrame will have no columns
    assert df.empty






