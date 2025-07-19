"""
Simple test file for code sniffer testing.
"""

def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    return length * width

def greet_user(name):
    """Greet a user with their name."""
    return f"Hello, {name}!"

class Calculator:
    """A simple calculator class."""
    
    def add(self, a, b):
        """Add two numbers."""
        return a + b
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

if __name__ == "__main__":
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"5 + 3 = {result}")
    
    area = calculate_area(10, 5)
    print(f"Area: {area}")
    
    greeting = greet_user("Patrick")
    print(greeting)
