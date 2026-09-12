# week_02_fundamentals/02_functions.py

#simple function
def greet_intern(name, week):
    message = f"Hello {name}, welcome to Week {week} of your internship!"
    return message

#simple function
def add_numbers(a, b):
    return a + b

# Call the functions
greeting = greet_intern("Alex", 2)
print(greeting)

result = add_numbers(5, 10)
print("5 + 10 =", result)