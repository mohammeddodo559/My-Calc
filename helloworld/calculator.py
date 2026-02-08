"""Calculator Engine for Streamlit Calculator Application.

This module provides the core arithmetic operations for the calculator.
"""


class Calculator:
    """Calculator engine that performs basic arithmetic operations."""
    
    def add(self, a: float, b: float) -> float:
        """Return sum of a and b.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            Sum of a and b
        """
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Return difference of a and b.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            Difference of a and b (a - b)
        """
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Return product of a and b.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            Product of a and b
        """
        return a * b
    
    def divide(self, a: float, b: float) -> tuple[float | None, str | None]:
        """Return quotient of a and b.
        
        Args:
            a: First operand (dividend)
            b: Second operand (divisor)
            
        Returns:
            Tuple of (result, error):
            - If successful: (quotient, None)
            - If division by zero: (None, error_message)
        """
        if b == 0:
            return None, "Division by zero is not allowed"
        return a / b, None
    
    def power(self, a: float, b: float) -> float:
        """Return a raised to the power of b."""
        return a ** b
    
    def sqrt(self, a: float) -> tuple[float | None, str | None]:
        """Return square root of a."""
        if a < 0:
            return None, "Cannot calculate square root of negative number"
        return a ** 0.5, None
    
    def sin(self, a: float) -> float:
        """Return sine of a (in radians)."""
        import math
        return math.sin(a)
    
    def cos(self, a: float) -> float:
        """Return cosine of a (in radians)."""
        import math
        return math.cos(a)
    
    def tan(self, a: float) -> float:
        """Return tangent of a (in radians)."""
        import math
        return math.tan(a)
    
    def log(self, a: float) -> tuple[float | None, str | None]:
        """Return natural logarithm of a."""
        import math
        if a <= 0:
            return None, "Cannot calculate log of non-positive number"
        return math.log(a), None
    
    def log10(self, a: float) -> tuple[float | None, str | None]:
        """Return base-10 logarithm of a."""
        import math
        if a <= 0:
            return None, "Cannot calculate log of non-positive number"
        return math.log10(a), None
    
    def factorial(self, a: float) -> tuple[float | None, str | None]:
        """Return factorial of a."""
        import math
        if a < 0 or a != int(a):
            return None, "Factorial only works with non-negative integers"
        return math.factorial(int(a)), None
    
    def calculate(self, a: float, operator: str, b: float = None) -> tuple[float | None, str | None]:
        """Perform calculation based on operator.
        
        Args:
            a: First operand
            operator: One of '+', '-', '*', '/', '^', 'sqrt', 'sin', 'cos', 'tan', 'ln', 'log', '!'
            b: Second operand (optional for unary operations)
            
        Returns:
            Tuple of (result, error):
            - If successful: (result, None)
            - If error: (None, error_message)
        """
        if operator == '+':
            return self.add(a, b), None
        elif operator == '-':
            return self.subtract(a, b), None
        elif operator == '*':
            return self.multiply(a, b), None
        elif operator == '/':
            return self.divide(a, b)
        elif operator == '^':
            return self.power(a, b), None
        elif operator == 'sqrt':
            return self.sqrt(a)
        elif operator == 'sin':
            return self.sin(a), None
        elif operator == 'cos':
            return self.cos(a), None
        elif operator == 'tan':
            return self.tan(a), None
        elif operator == 'ln':
            return self.log(a)
        elif operator == 'log':
            return self.log10(a)
        elif operator == '!':
            return self.factorial(a)
        else:
            return None, f"Invalid operator: {operator}"
