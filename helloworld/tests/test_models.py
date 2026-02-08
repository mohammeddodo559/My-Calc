"""Unit tests for data models."""

import pytest
from datetime import datetime
from models import CalculationRecord


class TestCalculationRecord:
    """Test suite for CalculationRecord class."""
    
    def test_to_dict_serialization(self):
        """Test conversion to dictionary for JSON serialization."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        record = CalculationRecord(
            operand1=5.0,
            operator='+',
            operand2=3.0,
            result=8.0,
            timestamp=timestamp
        )
        
        result = record.to_dict()
        
        assert result['operand1'] == 5.0
        assert result['operator'] == '+'
        assert result['operand2'] == 3.0
        assert result['result'] == 8.0
        assert result['timestamp'] == '2024-01-15T10:30:00'
    
    def test_from_dict_deserialization(self):
        """Test creation from dictionary."""
        data = {
            'operand1': 10.0,
            'operator': '-',
            'operand2': 4.0,
            'result': 6.0,
            'timestamp': '2024-01-15T14:45:30'
        }
        
        record = CalculationRecord.from_dict(data)
        
        assert record.operand1 == 10.0
        assert record.operator == '-'
        assert record.operand2 == 4.0
        assert record.result == 6.0
        assert record.timestamp == datetime(2024, 1, 15, 14, 45, 30)
    
    def test_round_trip_serialization(self):
        """Test that serialization and deserialization are inverse operations."""
        original = CalculationRecord(
            operand1=7.5,
            operator='*',
            operand2=2.0,
            result=15.0,
            timestamp=datetime(2024, 1, 15, 16, 20, 45)
        )
        
        # Serialize and deserialize
        data = original.to_dict()
        restored = CalculationRecord.from_dict(data)
        
        assert restored.operand1 == original.operand1
        assert restored.operator == original.operator
        assert restored.operand2 == original.operand2
        assert restored.result == original.result
        assert restored.timestamp == original.timestamp
    
    def test_format_expression_addition(self):
        """Test expression formatting for addition."""
        record = CalculationRecord(
            operand1=5.0,
            operator='+',
            operand2=3.0,
            result=8.0,
            timestamp=datetime.now()
        )
        
        expression = record.format_expression()
        assert expression == "5.0 + 3.0 = 8.0"
    
    def test_format_expression_subtraction(self):
        """Test expression formatting for subtraction."""
        record = CalculationRecord(
            operand1=10.0,
            operator='-',
            operand2=4.0,
            result=6.0,
            timestamp=datetime.now()
        )
        
        expression = record.format_expression()
        assert expression == "10.0 - 4.0 = 6.0"
    
    def test_format_expression_multiplication(self):
        """Test expression formatting for multiplication."""
        record = CalculationRecord(
            operand1=7.0,
            operator='*',
            operand2=6.0,
            result=42.0,
            timestamp=datetime.now()
        )
        
        expression = record.format_expression()
        assert expression == "7.0 * 6.0 = 42.0"
    
    def test_format_expression_division(self):
        """Test expression formatting for division."""
        record = CalculationRecord(
            operand1=20.0,
            operator='/',
            operand2=4.0,
            result=5.0,
            timestamp=datetime.now()
        )
        
        expression = record.format_expression()
        assert expression == "20.0 / 4.0 = 5.0"
    
    def test_format_expression_with_negative_numbers(self):
        """Test expression formatting with negative numbers."""
        record = CalculationRecord(
            operand1=-5.0,
            operator='+',
            operand2=-3.0,
            result=-8.0,
            timestamp=datetime.now()
        )
        
        expression = record.format_expression()
        assert expression == "-5.0 + -3.0 = -8.0"
    
    def test_format_expression_with_floats(self):
        """Test expression formatting with floating-point numbers."""
        record = CalculationRecord(
            operand1=3.14,
            operator='*',
            operand2=2.0,
            result=6.28,
            timestamp=datetime.now()
        )
        
        expression = record.format_expression()
        assert expression == "3.14 * 2.0 = 6.28"
    
    def test_timestamp_with_microseconds(self):
        """Test that timestamps with microseconds are handled correctly."""
        timestamp = datetime(2024, 1, 15, 10, 30, 45, 123456)
        record = CalculationRecord(
            operand1=1.0,
            operator='+',
            operand2=1.0,
            result=2.0,
            timestamp=timestamp
        )
        
        data = record.to_dict()
        restored = CalculationRecord.from_dict(data)
        
        assert restored.timestamp == timestamp
