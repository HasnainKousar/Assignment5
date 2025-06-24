#############################
# Calculator class #
#############################

"""
In this we will implement the main Calculator class that integrates 
all components, manages operations, history, observers, and configuration.


Key Concepts:

-Integration of Design Patterns: The Calculator class will utilize the
 Memento, Observer, and Strategy patterns to manage its operations and history.

-Data Persistence with pandas and csv: The Calculator will save its history
 to a CSV file using pandas, allowing for easy data manipulation and retrieval.

-Logging: The Calculator will log operations and errors using the logging module,
 providing a clear audit trail of all calculations performed.


"""

from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import List, Optional, Any, Dict, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation


Number = Union[int, float, Decimal]
CalculationResult = Union[Decimal, str]


class Calculator:    
    """
    Main Calculator class that integrates all components and manages operations, history, observers, and configuration.
    
    This class provides methods for performing calculations, managing history, and handling configuration.
    It uses the Memento pattern for undo/redo functionality and the Observer pattern for history management.
    """

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize the Calculator with a configuration object.

        Args:
            config (Optional[CalculatorConfig], optional): Configuration settings for the calculator.
                If not provided, default settings will be used.
        """
        # If no config is provided, use the default configuration
        if config is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir=project_root)

        # Assign the configuration and validate it
        self.config = config
        self.config.validate()

        # Assure that log directory exists
        os.makedirs(self.config.log_dir, exist_ok=True)


        #set up logging system
        self._setup_logging()

        #initialize history and operation strategy
        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None


        #initialize observers list
        self.observers: List[HistoryObserver] = []

        #initialize stacks for undo/redo functionality
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        #create required directories for history management
        self._setup_directories()

        try:
            #load history from file if it exists
            self.load_history()
        except Exception as e:
            # log a warning if history loading fails
            logging.warning(f"Could not load existing history: {e}")

            # Log the successful initialization of the calculator
        logging.info("Calculator initialized with configuration")


    def _setup_logging(self):
        """
        Configure the logging system for the calculator.
        
        Sets up the logging to a file with the specified format and level.

        """
        try:
            # make sure the log directory exists
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            #configure the basic logging settings
            logging.basicConfig(
                filename = str(log_file),
                level = logging.INFO,
                format = '%(asctime)s - %(levelname)s - %(message)s',
                force=True # force the logging configuration to be applied
            )
            logging.info(f"Logging initialized at: {log_file}")
        except Exception as e:
            print(f"Error setting up logging: {e}")
            raise

    def _setup_directories(self) -> None:
        """
        Create necessary directories.

        Ensure that all necessary directories for history management exist.

        """
        self.config.history_dir.mkdir(parents=True, exist_ok=True)


    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Register a new observer to the calculator.

        Adds an observer to the list of observers allowing it to receive updates
        when new calculations are performed.

        Args:
            observer (HistoryObserver): The observer to be added.
        
        """
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")

    
    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Remove an observer from the calculator.

        Args:
            observer (HistoryObserver): The observer to be removed.
        
        """
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        """
        Notify all observers about a new calculation.

        This method iterates through all registered observers and calls their
        update method with the new calculation.

        Args:
            calculation (Calculation): The Calculation instance to notify observers about.
        
        """
        for observer in self.observers:
            observer.update(calculation)
            
    def set_operation(self, operation: Operation) -> None:
        """
        Set the current operation strategy for the calculator.

        Assigns the provided operation as the current strategy for performing calculations.
        This allows the calculator to perform different types of calculations


        Args:
            operation (Operation): The operation to set as the current strategy.

        """
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    
    def perform_calculation(
            self,
            a: Union[str, Number],
            b: Union[str, Number],
    ) -> CalculationResult:
        """
        Perform a calculation using the current operation strategy.

        Validates and sanitizes the input, performs the calculation using
        the current operation strategy, updates the history, and notifies observers.

        Args:
            a (Union[str, Number]): The first operand for the calculation.
            b (Union[str, Number]): The second operand for the calculation.

        Returns:
            CalculationResult: The result of the calculation.

        Raises:
            ValidationError: If the input validation fails.
            OperationError: If the operation cannot be performed.
        """
        if not self.operation_strategy:
            raise OperationError("No operation set")
        
        try:
            #validate and convert inputs to Decimal
            validated_a = InputValidator.validate_number(a, self.config)
            validated_b = InputValidator.validate_number(b, self.config)

            #execute the operation strategy
            result = self.operation_strategy.execute(validated_a, validated_b)  


            # Create a new Calculation instance with the operation and operands
            calculation = Calculation(
                operation=str(self.operation_strategy),
                operand1=validated_a,
                operand2=validated_b,
            )

            # Save the current state to the undo stack before making changes
            self.undo_stack.append(CalculatorMemento(self.history.copy()))

            # Clear the redo stack since a new calculation is performed
            self.redo_stack.clear()

            # Append the new calculation to the history
            self.history.append(calculation)


            # make sure history does not exceed the maximum size
            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)  # remove the oldest calculation

            # Notify observers about the new calculation
            self.notify_observers(calculation)

            return result
        
        except ValidationError as e:
            # Log and re-raise validation errors
            logging.error(f"Validation error: {str(e)}")
            raise 
        except Exception as e:
            # Log and raise operation errors for any other exceptions
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")
        
    def save_history(self) -> None:
        """
        Save the current calculation history to a CSV file.

        Serializes the history of calculations to a CSV file for persistence storage.
        Use pandas for easy data manipulation and storage.

        Raises:
            OperationError: If the history cannot be saved.
        
        """
        try:
            # Ensure the history directory exists
            self.config.history_dir.mkdir(parents=True, exist_ok=True)

            history_data = []
            for calc in self.history:
                history_data.append({
                    'operation': str(calc.operation),
                    'operand1': str(calc.operand1),
                    'operand2': str(calc.operand2),
                    'result': str(calc.result),
                    'timestamp': calc.timestamp.isoformat()
                })
            
            if history_data:
                # Create a DataFrame from the history data
                df = pd.DataFrame(history_data)

                # Save the DataFrame to a CSV file
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")
            else:
                # if history is empty, create an empty CSV with headers
                pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp']).to_csv(
                    self.config.history_file, index=False
                )
                logging.info(f"Empty history file created at {self.config.history_file}")
        except Exception as e:
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")
    
    def load_history(self) -> None:
        """
        Load calculation history from a CSV file using pandas.
        
        Reads the history from the configured CSV file and reconstructs the Calculation
        instances, restoring them in the calculator's history.
        
        Raises:
            OperationError: If the history cannot be loaded or is invalid.
        """

        try:
            
            if self.config.history_file.exists():
                # Load the history from the CSV file
                df = pd.read_csv(self.config.history_file)

                if not df.empty:
                    # Deserialize each row into a Calculation instance
                    self.history = [
                        Calculation.from_dict({
                            "operation": row['operation'],
                            "operand1": row['operand1'],
                            "operand2": row['operand2'],
                            "result": row['result'],
                            "timestamp": row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]
                    logging.info(f"Loaded {len(self.history)} calculations from history")

                else:
                    logging.info("Loaded empty history file") # pragma: no cover

            else:
                logging.info("No History file found - starting with an empty histroy")
        
        except Exception as e:
            # Log and raise an OperationError if loading fails
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")
        
    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Get the current calculation history as a pandas DataFrame.

        Convert the list of Calculation instances into a pandas DataFrame for easy manipulation and analysis.

        Returns:
            pd.DataFrame: A DataFrame containing the calculation history.

        """
        history_data = []
        for calc in self.history:
            history_data.append({
                'operation': str(calc.operation),
                'operand1': str(calc.operand1),
                'operand2': str(calc.operand2),
                'result': str(calc.result),
                'timestamp': calc.timestamp.isoformat()
            })
        
        return pd.DataFrame(history_data)
    
    def show_history(self) -> None:
        """
        Get formated history of calculations.

        Returns a human-readable list of all calculations performed by the calculator.

        Returns:
            List[str]: A list of formatted calculation history entries.
        """

        return [
            f"{calc.operation}({calc.operand1}, {calc.operand2}) = {calc.result}"
            for calc in self.history
        ] # pragma: no cover
    
    def clear_history(self) -> None:
        """
        Clear the current calculation history.

        Resets the history to an empty list and clears the undo/redo stacks.


        """
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("Cleared calculation history")

    def undo(self) -> bool:
        """
        Undo the last calculation.

        Restores the calculator's state to the previous memento, effectively undoing the last operation.
        
        Returns:
            bool: True if the undo was successful, False if there are no actions to undo.
        
        """
        if not self.undo_stack:
            return False  # No actions to undo #pragma: no cover
        
        # Pop the last memento from the undo stack
        memento = self.undo_stack.pop()
        # push the current state to the redo stack
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        # Restore the history from the memento
        self.history = memento.history.copy()
        return True
    

    def redo(self) -> bool:
        """
        Redo the last undone calculation.

        Restores the calculator's state to the next memento, effectively redoing the last undone operation.
        
        Returns:
            bool: True if the redo was successful, False if there are no actions to redo.
        
        """
        if not self.redo_stack:
            return False # pragma: no cover
        # Pop the last memento from the redo stack
        memento = self.redo_stack.pop()
        # Push the current state to the undo stack
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        # Restore the history from the memento
        self.history = memento.history.copy()
        return True
    


