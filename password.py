import re

def check_password_strength(password):
    length_condition = len(password) >= 8
    uppercase_condition = any(char.isupper() for char in password)
    lowercase_condition = any(char.islower() for char in password)
    number_condition = any(char.isdigit() for char in password)
    special_char_condition = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    strength = sum([length_condition, uppercase_condition, lowercase_condition, number_condition, special_char_condition])
    if strength == 5:
        return "Very Strong"
    elif strength >= 3:
        return "Strong"
    elif strength >= 2:
        return "Moderate"
    elif strength >= 1:
        return "Weak"
    else:
        return "Very Weak"
password_input = input("Enter your password: ")
strength_result = check_password_strength(password_input)
print(f"Password Strength: {strength_result}")
