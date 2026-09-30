#ask user for their name and greet them
name = input("Whats your name? ")
#Remove any leading or trailing whitespace from the name and capitalize the first letter of each word in the name
name = name.strip().title()
#split the name into a first name and last name.
name_parts = name.split()
print(f"Hello, {name}!")
print(f"First name: {name_parts[0]}")
print(f"Last name: {name_parts[-1]}")
age = input("How old are you? ")
#Check if the age is a valid number
if age.isdigit():
    age = int(age)
    print(f"You are {age} years old.")

#ask the user for their parentage
parentage = input("What is your parentage? ")
#Remove any leading or trailing whitespace from the parentage and capitalize the first letter of each word
parentage = parentage.strip().title()
print(f"Your parentage is: {parentage}")
    