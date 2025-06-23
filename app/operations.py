# Operation Classes


from abc import ABC, abstractmethod
from typing import Dict
from decimal import Decimal


class Operation(ABC):
    """
    Abstract base class for operations.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the operation.

        Performs the opertion with the given operands.

        args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.

        returns:
            Decimal: The result of the operation.

        raises:
            OperationError: If the operation cannot be performed.

        """
        pass # pragma: no cover


    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution.

        This can be overridden by subclasses to add 
        specific validation rules for different operations.

        args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.
        
        raises:
            ValueError: If the operands are invalid.
        """
        pass  

    def __str__(self) -> str:
        """
        String representation of the operation, typically the class name.

        Returns a string that describes the operation.

        returns:
            str: The name of the operation class.
        """
        return self.__class__.__name__
    

class Add(Operation):
    """
    Addition operation.

    Performs addition of two Decimal numbers.
        
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Add two Decimal numbers.

        args:
            a (Decimal): The first operand.
            b (Decimal): The second operand. 

        Returns:
            Decimal: The sum of a and b.    

        """
        self.validate_operands(a, b)
        return a + b
        
class Subtract(Operation):
    """
    Subtraction operation.

    Performs subtraction of two Decimal numbers.
        
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Subtract two Decimal numbers.

        args:
            a (Decimal): The first operand.
            b (Decimal): The second operand. 

        Returns:
            Decimal: The difference of a and b.    

        """
        self.validate_operands(a, b)
        return a - b
    
class Multiply(Operation):
    """
    Multiplication operation.

    Performs multiplication of two Decimal numbers.
        
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Multiply two Decimal numbers.

        args:
            a (Decimal): The first operand.
            b (Decimal): The second operand. 

        Returns:
            Decimal: The product of a and b.    

        """
        self.validate_operands(a, b)
        return a * b
    


        
        
  