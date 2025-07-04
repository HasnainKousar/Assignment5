############################
# Calculator Configuration #
############################

from dataclasses import dataclass
from decimal import Decimal
from email.policy import default
from numbers import Number
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

#load environment variables from .env file
load_dotenv()

def get_project_root() -> Path:
    """
    Get the root directory of the project.
    
    This function determines the root directory of the project by checking
    the current working directory and adjusting it to find the 'app' directory.
    
    Returns:
        Path: The root directory of the project.
    """
    # Get the current working directory
    current_file = Path(__file__)
    # Traverse up to the root directory where 'app' is located
    return current_file.parent.parent


@dataclass
class CalculatorConfig:
    """
    Configuration for the calculator application.
    
    This class holds configuration settings for the calculator, including
    the precision for decimal operations, directory paths, history size, 
    auto-save preference, maximum input values, and default encoding.
    
    Configurations are loaded from environment variables or by passing
    parameters directly to the class constructor.
    
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None,
    ):
        """
        Initialize the CalculatorConfig with default or provided values.
        
        Args:
            base_dir (Path, optional): Base directory for the application.
            max_history_size (int, optional): Maximum size of the calculation history.
            auto_save (bool, optional): Whether to auto-save the calculation history.
            precision (int, optional): Decimal precision for calculations.
            max_input_value (Number, optional): Maximum value for input operands.
            default_encoding (str, optional): Default encoding for string operations.
        """
       
       # Set base directory to project root by default
        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv("CALCULATOR_BASE_DIR", str(project_root))
        ).resolve()


        # Maximum size of the calculation history
        self.max_history_size = max_history_size or int(
            os.getenv("CALCULATOR_MAX_HISTORY_SIZE", '1000')
        )


        # Auto-save preference for the calculation history
        auto_save_env = os.getenv("CALCULATOR_AUTO_SAVE", 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )


        # Decimal precision for calculations
        self.precision = precision or int(os.getenv("CALCULATOR_PRECISION", '10'))


        # Maximum value for input operands
        self.max_input_value = max_input_value or Decimal(
            os.getenv("CALCULATOR_MAX_INPUT_VALUE", '1000000')
        )


        # Default encoding for string operations
        self.default_encoding = default_encoding or os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", 'utf-8'
        )


    @property
    def log_dir(self) -> Path:
        """
        Get the log directory path.
            
        Determines the directory path where log files will be stored.

        Returns:
            Path: The path to the log directory. 
        """
        return Path(os.getenv(
            "CALCULATOR_LOG_DIR",
            str(self.base_dir / "logs")
        )).resolve()
    
    @property
    def history_dir(self) -> Path:
        """
        Get the history directory path.

        Determines the directory path where calculation history files will be stored.

        Returns:
            Path: The path to the history directory.
        """
        return Path(os.getenv(
            "CALCULATOR_HISTORY_DIR",
            str(self.base_dir / "history")
        )).resolve()
    

    @property
    def history_file(self) -> Path:
        """
        Get the path to the history file.

        Determines te file path for storing the calculation history in CSV format.

        Returns:
            Path: The path to the history file.
        """
        return Path(os.getenv(
            "CALCULATOR_HISTORY_FILE",
            str(self.history_dir / "calculator_history.csv")
        )).resolve()
    

    @property
    def log_file(self) -> Path:
        """
        Get the path to the log file.

        Determines the file path for storing log entries.

        Returns:
            Path: The path to the log file.
        """
        return Path(os.getenv(
            "CALCULATOR_LOG_FILE",
            str(self.log_dir / "calculator.log")
        )).resolve()
    

    def validate(self) -> None:
        """
        Validate the configuration settings.

        This method checks if the configuration settings are valid, such as ensuring
        that the base directory exists and that the precision is a positive integer.
        
        Raises:
            ConfigurationError: If any configuration setting is invalid.
        """
        if self.max_history_size <= 0:
            raise ConfigurationError("Maximum history size must be a positive.")
        if self.precision <= 0:
            raise ConfigurationError("Precision must be a positive integer.")
        if self.max_input_value <= 0:
            raise ConfigurationError("Maximum input value must be a positive number.")
        

        
