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



