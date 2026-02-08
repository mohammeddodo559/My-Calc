"""Data models for Streamlit Calculator Application.

This module provides data classes for representing calculation records.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalculationRecord:
    """Represents a single calculation record with timestamp.
    
    Attributes:
        operand1: First operand in the calculation
        operator: The arithmetic operator (+, -, *, /)
        operand2: Second operand in the calculation
        result: The result of the calculation
        timestamp: When the calculation was performed
    """
    operand1: float
    operator: str
    operand2: float
    result: float
    timestamp: datetime
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation with ISO format timestamp
        """
        return {
            'operand1': self.operand1,
            'operator': self.operator,
            'operand2': self.operand2,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CalculationRecord':
        """Create instance from dictionary.
        
        Args:
            data: Dictionary containing calculation record data
            
        Returns:
            CalculationRecord instance
        """
        return cls(
            operand1=data['operand1'],
            operator=data['operator'],
            operand2=data['operand2'],
            result=data['result'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
    
    def format_expression(self) -> str:
        """Format as readable expression.
        
        Returns:
            Formatted string like '5 + 3 = 8'
        """
        return f"{self.operand1} {self.operator} {self.operand2} = {self.result}"
