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


def test_auto_save_env_var_true():
    
    os.environ['CALCULATOR_AUTO_SAVE'] = 'true'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is True



def test_auto_save_env_var_false():
    os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is False


def test_auto_save_env_var_is_one():
    os.environ['CALCULATOR_AUTO_SAVE'] = '1'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is True

def test_auto_save_env_var_is_zero():
    os.environ['CALCULATOR_AUTO_SAVE'] = '0'
    config = CalculatorConfig(auto_save=None)
    assert config.auto_save is False


def test_enviroment_overrides():
    config = CalculatorConfig()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 4
    assert config.max_input_value == Decimal('1000')
    assert config.default_encoding == 'utf-16'


def test_default_fallbacks():
    #clear all related environment variables and test defaults
    clear_env_vars(
        'CALCULATOR_MAX_HISTORY_SIZE',
        'CALCULATOR_AUTO_SAVE',
        'CALCULATOR_PRECISION',
        'CALCULATOR_MAX_INPUT_VALUE',
        'CALCULATOR_DEFAULT_ENCODING'
    )

    config = CalculatorConfig()
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal('1000000')
    assert config.default_encoding == 'utf-8'

def test_get_project_root():
    """Test if get_project_root returns the correct path."""
    from app.calculator_config import get_project_root
    assert (get_project_root() / 'app').exists()


def test_log_dir_property():
    # clear the environment variable to test default behavior
    clear_env_vars('CALCULATOR_LOG_DIR')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.log_dir == Path('/new_base_dir/logs').resolve()

def test_history_dir_property():
    # clear the environment variable to test default behavior
    clear_env_vars('CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.history_dir == Path('/new_base_dir/history').resolve()


def test_history_file_property():
    # clear the environment variable to test default behavior
    clear_env_vars('CALCULATOR_HISTORY_FILE')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.history_file == Path('/new_base_dir/history/calculator_history.csv').resolve()


def test_log_file_property():
    # clear the environment variable to test default behavior
    clear_env_vars('CALCULATOR_LOG_FILE')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.log_file == Path('/new_base_dir/logs/calculator.log').resolve()


