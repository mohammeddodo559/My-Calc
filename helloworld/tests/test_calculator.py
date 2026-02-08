"""Unit tests for Calculator class."""

import pytest
from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    # Addition tests
    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        result = self.calc.add(5, 3)
        assert result == 8
    
    def test_add_negative_numbers(self):
        """Test addition of negative numbers."""
        result = self.calc.add(-5, -3)
        assert result == -8
    
    def test_add_mixed_signs(self):
        """Test addition of numbers with different signs."""
        result = self.calc.add(5, -3)
        assert result == 2
    
    # Subtraction tests
    def test_subtract_positive_numbers(self):
        """Test subtraction of positive numbers."""
        result = self.calc.subtract(10, 3)
        assert result == 7
    
    def test_subtract_negative_numbers(self):
        """Test subtraction of negative numbers."""
        result = self.calc.subtract(-5, -3)
        assert result == -2
    
    def test_subtract_mixed_signs(self):
        """Test subtraction with mixed signs."""
        result = self.calc.subtract(5, -3)
        assert result == 8
    
    # Multiplication tests
    def test_multiply_positive_numbers(self):
        """Test multiplication of positive numbers."""
        result = self.calc.multiply(4, 5)
        assert result == 20
    
    def test_multiply_negative_numbers(self):
        """Test multiplication of negative numbers."""
        result = self.calc.multiply(-4, -5)
        assert result == 20
    
    def test_multiply_mixed_signs(self):
        """Test multiplication with mixed signs."""
        result = self.calc.multiply(4, -5)
        assert result == -20
    
    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        result = self.calc.multiply(5, 0)
        assert result == 0
    
    # Division tests
    def test_divide_positive_numbers(self):
        """Test division of positive numbers."""
        result, error = self.calc.divide(10, 2)
        assert result == 5
        assert error is None
    
    def test_divide_negative_numbers(self):
        """Test division of negative numbers."""
        result, error = self.calc.divide(-10, -2)
        assert result == 5
        assert error is None
    
    def test_divide_mixed_signs(self):
        """Test division with mixed signs."""
        result, error = self.calc.divide(10, -2)
        assert result == -5
        assert error is None
    
    def test_divide_by_zero(self):
        """Test division by zero returns error."""
        result, error = self.calc.divide(10, 0)
        assert result is None
        assert error == "Division by zero is not allowed"
    
    def test_divide_zero_by_number(self):
        """Test zero divided by a number."""
        result, error = self.calc.divide(0, 5)
        assert result == 0
        assert error is None
    
    # Calculate method tests
    def test_calculate_addition(self):
        """Test calculate method with addition operator."""
        result, error = self.calc.calculate(5, '+', 3)
        assert result == 8
        assert error is None
    
    def test_calculate_subtraction(self):
        """Test calculate method with subtraction operator."""
        result, error = self.calc.calculate(10, '-', 3)
        assert result == 7
        assert error is None
    
    def test_calculate_multiplication(self):
        """Test calculate method with multiplication operator."""
        result, error = self.calc.calculate(4, '*', 5)
        assert result == 20
        assert error is None
    
    def test_calculate_division(self):
        """Test calculate method with division operator."""
        result, error = self.calc.calculate(10, '/', 2)
        assert result == 5
        assert error is None
    
    def test_calculate_division_by_zero(self):
        """Test calculate method handles division by zero."""
        result, error = self.calc.calculate(10, '/', 0)
        assert result is None
        assert error == "Division by zero is not allowed"
    
    def test_calculate_invalid_operator(self):
        """Test calculate method with invalid operator."""
        result, error = self.calc.calculate(5, '%', 3)
        assert result is None
        assert error == "Invalid operator: %"
    
    # Floating-point precision tests
    def test_add_floats(self):
        """Test addition with floating-point numbers."""
        result = self.calc.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-10
    
    def test_divide_floats(self):
        """Test division with floating-point numbers."""
        result, error = self.calc.divide(1.0, 3.0)
        assert error is None
        assert abs(result - 0.3333333333333333) < 1e-10
