"""
Calculator Memento

In this module, we define the `CalculatorMemento` class, which is used to store the state of the calculator.
This class is part of the memento design pattern, allowing us to store calculator states
for undo/redo functionality.

key features:
- Memento design pattern: Captures and stores the state of the calculator without exposing its internal structure.
- Serialization and deserialization: convert mementos to and from a dictionaries for prersistence.
"""

from dataclasses import dataclass, field
import datetime
from typing import Dict, Any, List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    """
    Stores calculator state for undo/redo functionality.
    
    The Memento patterns allows the calculator to save its current state (history of calculations)
    so that it can be restored later. This is useful for implementing undo/redo features.
    """

    history: List[Calculation] # List of Calculation objects representing the history of calculations
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)  # Timestamp of when the memento was created

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert memento to a dictionary.

        This method serializes the memento's state into a dictionary format,
        which can be used for storage or transmission.
        
        Returns:
            Dict[str, Any]: A dictionary containing the serialized state of the memento.
        """
        return {
            "history": [calc.to_dict() for calc in self.history],
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalculatorMemento":
        """
        Create a calculator memento from a dictionary.
        
        This class method deserializes a dictionary to recreate a CalculatorMemento instance,
        restoring the history of calculations and the timestamp.
        
        
        Args:
            data (Dict[str, Any]): A dictionary containing the serialized state of the memento.
            
        
        Returns:
            CalculatorMemento: A new instance of CalculatorMemento with the state restored from the dictionary.
        """

        return cls(
            history=[Calculation.from_dict(calc) for calc in data["history"]],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"])
        )
    
