# Tests for the config module

from logging import config
import pytest
import os
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

# set temporary environment variables for testing

os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '500'
os.environ['CALCULATOR_AUTO_SAVE'] = 'True'
os.environ['CALCULATOR_PRECISION'] = '4'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-16'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'


#helper function to clear specific environment variables
def clear_env_vars(*args):
    for var in args:
        os.environ.pop(var, None)


def test_custom_config():
    """Test custom configuration settings."""
    config = CalculatorConfig(
        max_history_size=1000,
        auto_save=True,
        precision=6,
        max_input_value=Decimal('5000'),
        default_encoding='ascii',
    )
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 6
    assert config.max_input_value == Decimal('5000')
    assert config.default_encoding == 'ascii'


def test_directory_properties():
    """Test directory properties."""
    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/test_base'))
    assert config.history_dir == Path('/test_base/history').resolve()
    assert config.log_dir == Path('/test_base/logs').resolve()


def test_file_properties():
    """Test file properties."""
    clear_env_vars('CALCULATOR_LOG_FILE', 'CALCULATOR_HISTORY_FILE')
    config = CalculatorConfig(base_dir=Path('./test_base'))
    assert config.history_file == Path('./test_base/history/calculator_history.csv').resolve()
    assert config.log_file == Path('./test_base/logs/calculator.log').resolve()


def test_invalid_max_history_size():
    """Test invalid max history size."""
    with pytest.raises(ConfigurationError, match="Maximum history size must be a positive."):
        config = CalculatorConfig(max_history_size=-1)
        config.validate()


def test_invalid_precision():
    """Test invalid precision."""
    with pytest.raises(ConfigurationError, match="Precision must be a positive integer."):
        config = CalculatorConfig(precision=-1)
        config.validate()


def test_invalid_max_input_value():
    """Test invalid maximum input value."""
    with pytest.raises(ConfigurationError, match="Maximum input value must be a positive number."):
        config = CalculatorConfig(max_input_value = -1)
        config.validate()

