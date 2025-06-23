######################
# Calculation Model  #
######################


from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError

@dataclass
class Calculation:
    """
    Value object representing a single calculation.
    
    This class encapsulates the details of a calculation, including the
    operands, the operation performed, the result, and timestamps of calculation.
    It provided methods for performing the calculation, serializing the data for storage,
    and deserializing data to restore the calculation instance."""

    #required fields
    operation: str
    operand1: Decimal
    operand2: Decimal


    #fields with default values
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)


    def __post_init__(self):
        """
        Post-initialization processing.

        Automatically calculates the result of the operation after the Calculation
        instance is created.
        """
        self.result = self.calculate()

    def calculate(self) -> Decimal:
        """
        Execute the calculation using the specified operation.
            
        utilizes a dictionary to map operation names to their corresponding lambda functions,
        enabling dynamic execution of the operation based on the operation name.
        
        returns:
            Decimal: The result of the calculation.
            
        raises:
            OperationError: If the operation is not recognized or if an error occurs during calculation.
        
        """
        operations = {
            "Addition": lambda a, b: a + b,
            "Subtraction": lambda a, b: a - b,
            "Multiplication": lambda a, b: a * b,
            "Division": lambda a, b: a / b if b != 0 else self._raise_div_zero(),
            "Power": lambda a, b: Decimal(pow(float(a), float(b))) if b >= 0 else self._raise_neg_power(),
            "Root": lambda a, b: (
                Decimal(pow(float(a), 1 / float(b)))
                if a >= 0 and b != 0
                else self._raise_invalid_root(a, b)
            )
        }

        #retrieve the operation function based on the operation name
        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")
            
        try:
            #execute the operation and return the result
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            #handle any errors that occur during calculation
            raise OperationError(f"Calculation Failed: {str(e)}")
            

    @staticmethod
    def _raise_div_zero(): # pragma: no cover
        """
        Helper method to raise an error for division by zero.

        This method is used to raise an OperationError when a division by zero is attempted.
        """
        raise OperationError("Division by zero is not allowed.")
    
    @staticmethod
    def _raise_neg_power(): # pragma: no cover
        """
        Helper method to raise an error for negative power.

        This method is used to raise an OperationError when a negative power is attempted.
        """
        raise OperationError("Exponent must be non-negative.")
    
    @staticmethod
    def _raise_invalid_root(a: Decimal, b: Decimal): # pragma: no cover
        """
        Helper method to raise an error for invalid root calculation.

        This method is used to raise an OperationError when the root calculation is invalid,
        such as when the base is negative or the root degree is zero.
        

        args:
            a (Decimal): The base number for the root calculation.
            b (Decimal): The degree of the root.    
        """
        if b == 0:
            raise OperationError("Zero root is not defined.")
        if a < 0:
            raise OperationError("cannot calculate root of a negative number.")
        raise OperationError("Invalid root operation.")
    

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the Calculation instance to a dictionary.

        This method converts the Calculation instance into a dictionary format,
        which can be used for storage or transmission.
        
        returns:
            Dict[str, Any]: A dictionary representation of the Calculation instance.
        """
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Calculation":
        """
        Create a Calculation instance from a dictionary.
        
        This method reconstructs a Calculation instance from a dictionary,
        ensuring that all required fields are present and correctly formatted.
        
        args:
            data (Dict[str, Any]): A dictionary containing the calculation data.
            
        returns:
            Calculation: A new Calculation instance with data populated from the dictionary.
            
        raises:
            OperationError: If the data is missing required fields or contains invalid values.
        """

        try: 
            # Create the calculation object with the original operands
            calc = Calculation(
                operation=data["operation"],
                operand1=Decimal(data["operand1"]),
                operand2=Decimal(data["operand2"])
            )

            #set the timestamp from the saved data
            calc.timestamp = datetime.datetime.fromisoformat(data["timestamp"])

            #verify the result matches the calculation
            saved_result = Decimal(data["result"])
            if calc.result != saved_result:
                logging.warning(
                    f'Loaded calculation result {saved_result} '
                    f'differs from computed result {calc.result}'
                ) # pragma: no cover

            return calc
        except (KeyError, ValueError, InvalidOperation) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")
        
        
    def __str__(self) -> str:
        """
        Return a string representation of the Calculation instance.
        
        Provides a human-readable format of the calculation, including the operation,
        operands, result, and timestamp.
        
        
        returns:
            str: A string representation of the Calculation instance.
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the Calculation instance.

        Provides a detailed and unambiguous string representation of the Calculation
        instance, useful for debugging.

        returns:
            str: A detailed string representation of the Calculation instance.
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"

        )
    
    def __eq__(self, other: Any) -> bool:
        """
        Check if two calculations are equal.
        
        Compares two calculation instances to determine if they represent the
        same operation with the same operands and result.
        
        
        Args:
            other (object): Another calculation to compare with.
            
        Returns:
            bool: True if the calculations are equal, False otherwise.
            
        """
        if not isinstance(other, Calculation):
            return False
        
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )
    

    def format_result(self, precision: int = 10) -> str:
        """
        Format the result of the calculation to a specified precision.
        
        This method formats the result of the calculation to a string with a specified
        number of decimal places, ensuring consistent output for display or storage.
        
        Args:
            precision (int): The number of decimal places to format the result to.
            
        Returns:
            str: The formatted result as a string.
        """
        try: 
            #remove trailing zeros and format the result
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation:  # pragma: no cover
            return str(self.result)
        