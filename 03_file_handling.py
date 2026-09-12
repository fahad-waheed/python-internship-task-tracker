# week_02_fundamentals/03_file_handling.py

file_name = "week_02_fundamentals/notes.txt"

# 1. Write to a file
print("Writing to file...")
with open(file_name, "w") as file:
    file.write("Week 2: Learning Python fundamentals.\n")
    file.write("Today I practiced file handling.\n")

# 2. Read from the file
print("Reading from file...")
with open(file_name, "r") as file:
    content = file.read()
    print("\n--- File Contents ---")
    print(content)