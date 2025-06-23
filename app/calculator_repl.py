#######################
# Advanced Calculator REPL
#######################

"""
THis module provides an advanced REPL (Read-Eval-Print Loop) for the calculator application.
It allows users to interactively perform calculations, manage history, and utilize advanced features like undo/
redo functionality.

"""

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def run_calculator_repl():

    """
    Command-line interface for the advanced calculator.

    Implements a REPL (Read-Eval-Print Loop) for the calculator application,
    that continuously prompts the user for commands, processes arthemetic operations,
    and manages the calculator's history.
    
    """

    try: 
        # Initialize the calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Welcome to the Advanced Calculator REPL!")
        print("Type 'help' for a list of commands")

        # Main REPL loop
        while True:
            try:
                # prompt the user for the command
                command = input("\nEnter command: ").strip().lower()

                if command == 'help':
                    #display available commands
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root - Perform arithmetic operations")
                    print("  history - Show calculation history")
                    print("  undo - Undo the last operation")
                    print("  redo - Redo the last undone operation")
                    print("  clear - Clear the history")
                    print("  save - Save the current history to a file")
                    print("  load - Load history from a file")
                    print("  exit - Exit the calculator REPL")
                    continue
                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history before exiting: {e}")
                    print("Exiting the calculator REPL. Goodbye!")
                    break
                if command == 'history':
                    # Display the calculation history
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history.")
                    else:
                        print("\nCalculation History:")
                        for idx, entry in enumerate(history, start=1):
                            print(f"{idx}: {entry}")
                    continue

                if command == 'clear':
                    # Clear the calculation history
                    calc.clear_history()
                    print("History cleared.")
                    continue

                if command == 'undo':
                    # Undo the last operation
                    if calc.undo():
                        print("Last operation undone.")
                    else:
                        print("No operation to undo.")
                    continue

                if command == 'redo':
                    # Redo the last undone operation
                    if calc.redo():
                        print("Last operation redone.")
                    else:
                        print("No operation to redo.")
                    continue

                if command == 'load':
                    # Load history from a file
                    try:
                        calc.load_history()
                        print("History loaded successfully.")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                if command == 'save':
                    # Save the current history to a file
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root']:
                    # perform the specified arithmetic operation
                    try:
                        print("\n Enter number (or cancel to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled.")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled.")
                            continue

                        # Create the appropriate operation instance usin the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)


                        # Perform the calculation
                        result = calc.perform_calculation(a,b)

                        # Normalize the result if it is a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")

                    except (OperationError, ValidationError) as e:
                        # Handle specific operation errors
                        print(f"Error: {e}")

                    except Exception as e:
                        # Handle any other unexpected errors
                        print(f"An unexpected error occurred: {e}")
                    continue

                # Handle unknown commands
                print(f"Unknown command: {command}. Type 'help' for a list of commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\nOperation cancelled")
                continue

            except EOFError:
                # Handle Ctrl+D gracefully
                print("\nInput terminated. Exiting the calculator REPL.")
                break
            except Exception as e:
                # Handle any other unexpected errors
                print(f"An unexpected error occurred: {e}")
                continue

    except Exception as e:
        # Handle any initialization errors
        print(f"An error occurred while starting the calculator: {e}")
        logging.error(f"Calculator initialization failed: {e}")
        raise


# if you want to run the REPL directly, uncomment the following lines:
# if __name__ == "__main__":
#     # Run the calculator REPL if this script is executed directly
#     run_calculator_repl()







