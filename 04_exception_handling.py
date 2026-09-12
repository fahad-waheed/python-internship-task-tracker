# week_02_fundamentals/04_exception_handling.py

print("--- Exception Handling Demo ---")

# 1. Trying to divide by zero
try:
    number = 10
    result = number / 0
    print("Result:", result)
except ZeroDivisionError:
    print("Oops! You cannot divide a number by zero.")

# 2. Trying to open a file that doesn't exist
try:
    with open("missing_file.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Oops! That file does not exist.")

print("Program finished successfully without crashing!")