# week_02_fundamentals/01_fundamentals.py

# 1.Variables (Strings, Integers, Booleans)
intern_name = "Alex"
current_week = 2
is_internship_active = True

# 2.List
skills_learned = ["Python basics", "Git", "VS Code"]

# 3.Dictionary
intern_info = {
    "name": intern_name,
    "week": current_week,
    "active": is_internship_active
}

# 4. Print and Loop
print("--- Intern Information ---")
print("Name:", intern_info["name"])
print("Current Week:", intern_info["week"])

print("\n--- Skills Learned ---")
for skill in skills_learned:
    print("-", skill)