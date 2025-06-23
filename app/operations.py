# Operation Classes


from abc import ABC, abstractmethod
from typing import Dict
from decimal import Decimal
from app.exceptions import ValidationError




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
    

class Addition(Operation):
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
        
class Subtraction(Operation):
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
    
class Multiplication(Operation):
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
    

class Division(Operation):
    """
    Division operation.

    Performs division of two Decimal numbers.
        
    """
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution.

        This can be overridden by subclasses to add 
        specific validation rules for different operations.

        args:
            a (Decimal): The dividend.
            b (Decimal): The divisor.
        
        raises:
            ValueError: If the operands are invalid.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Divide a by b.

        args:
            a (Decimal): The dividend.
            b (Decimal): The divisor. 

        Returns:
            Decimal: The result of a divided by b.    

        raises:
            ValidationError: If the divisor is zero.
        """
        self.validate_operands(a, b)
        return a / b
    

        
class Power(Operation):
    """
    Power operation.

    Raises the first Decimal number to the power of the second.
        
    """
   

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution.

        This can be overridden by subclasses to add 
        specific validation rules for different operations.

        args:
            a (Decimal): The base.
            b (Decimal): The exponent.
        
        raises:
            ValueError: If the operands are invalid.
        """
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Exponent must be non-negative.")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Raise a to the power of b.

        args:
            a (Decimal): The base.
            b (Decimal): The exponent. 

        Returns:
            Decimal: The result of a raised to the power of b.    

        raises:
            ValidationError: If the exponent is negative.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))
        
class Root(Operation):
    """
    Root operation.

    Calculates the nth root of a Decimal number.
        
    """
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution.

        This can be overridden by subclasses to add 
        specific validation rules for different operations.

        args:
            a (Decimal): The number to find the root of.
            b (Decimal): The degree of the root.

        raises:
            ValidationError: If the number is negative or the root degree is zero.

        """
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("cannot calculate root of a negative number.")
        if b == 0:
            raise ValidationError("Zero root is not defined.")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the nth root of a.

        args:
            a (Decimal): The number to find the root of.
            b (Decimal): The degree of the root. 

        Returns:
            Decimal: The nth root of a.

        raises:
            ValidationError: If the number is negative or the root degree is zero.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))
    



class OperationFactory:
    """
    Factory class to create operation instances based on the operation name.
    """

    _operations: Dict[str, type] = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Register a new operation class.

        args:
            name (str): The name of the operation.
            operation_class (type): The class implementing the operation.

        raises:
            TypeError: If operation_class is not a subclass of Operation.

        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation.")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an operation instance based on the operation type.

        This method retrieves the appropriate operation class from the
        _operations dictionary and returns an instance of it.

        Args:
            operation_type (str): The type of operation to create (e.g., "add", "subtract").

        Returns:
            Operation: An instance of the requested operation class.

        Raises:
            ValueError: If the operation type is not recognized.
        """
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown Operation: {operation_type}")
        return operation_class()
    

