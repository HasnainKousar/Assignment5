########################
# Exception Hierarchy  #
########################

class CalculatorError(Exception):
    """
    Base class for all calculator-related exceptions.
    
    This exception serves as the base class for all custom exceptions 
    related to calculator operations, providing a common interface for 
    error handling.
    
    """

    pass



class ValidationError(CalculatorError):
    """
    
    Raised when input validation fails.

    This exception is used to indicate that the input provided to a 
    calculator operation does not meet the required validation criteria.

    """
    pass

class OperationError(CalculatorError):
    """
    Raised when a calculation operation fails.

    This exception is used to indicate failure during the execution of 
    arthmetic operations, such as division by zero or invalid operations.

    """
    pass

class ConfigurationError(CalculatorError):
    """
    Raised when there is a configuration issue.

    This exception is used to indicate that there is a problem with the 
    configuration of the calculator, such as missing or invalid settings.

    """
    pass


