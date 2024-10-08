This project provides a simple calculator class that can perform basic arithmetic operations and root calculations.

Class: Calculator
The Calculator class performs the following operations:

Addition
Subtraction
Multiplication
Division
Nth Root Calculation

Methods:

__init__(self, number_1: float, number_2: float): Initializes the calculator with two numbers.
add(self) -> float: Adds the two numbers.
subtract(self) -> float: Subtracts the second number from the first number.
multiply(self) -> float: Multiplies the two numbers.
divide(self) -> float: Divides the first number by the second number.
nroot(self) -> float: Calculates the nth root of the first number based on the second number.
decision(self, user_decision: str) -> float: Performs the operation based on the user's decision.
reset(self): Resets the memory to zero.

Installation
To install the project, you need to have Python installed. Then, you can set up the project using pyproject.toml.


Example Usages; 
from calculator.calculator import Calculator

# Create a Calculator object
calc = Calculator(10, 5)

# Perform operations
print(calc.add().memory)       # Output: 15
print(calc.subtract().memory)  # Output: 5
print(calc.multiply().memory)  # Output: 50
print(calc.divide().memory)    # Output: 2.0
print(calc.nroot().memory)     # Output: 1.5848931924611136

# Chaining operations
calc.reset().number_1 = 10
calc.number_2 = 5
print(calc.add().subtract().multiply().divide().memory)  # Output: 2.0

# Reset the calculator
calc.reset()
print(calc.memory)      # Output: 0.0

# Print calculator value
print(str(calc))        # Output: 0.0
