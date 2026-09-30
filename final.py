# Password Strength Checker
# Checks passwords for different apps, gives feedback,
# and warns if the same password is used in more than one app.

import string
import secrets

common_passwords = ["password", "123456", "12345678", "qwerty", "abc123",
                    "admin", "letmein", "welcome", "iloveyou", "password123"]


def check_password(password):
    score = 0
    tips = []

    if password.lower() in common_passwords:
        tips.append("This is a very common password. Hackers try these first! Change it fully.")
        return 0, tips

    if len(password) >= 12:
        score = score + 2
    elif len(password) >= 8:
        score = score + 1
        tips.append("Make it at least 12 characters long.")
    else:
        tips.append("Too short! Use at least 8 characters (12 or more is better).")

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for ch in password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
        else:
            has_special = True

    if has_upper:
        score = score + 1
    else:
        tips.append("Add at least one UPPERCASE letter.")

    if has_lower:
        score = score + 1
    else:
        tips.append("Add at least one lowercase letter.")

    if has_digit:
        score = score + 1
    else:
        tips.append("Add at least one number.")

    if has_special:
        score = score + 1
    else:
        tips.append("Add at least one special character like ! @ # $ %")

    for i in range(len(password) - 2):
        if password[i] == password[i + 1] and password[i] == password[i + 2]:
            score = score - 1
            tips.append("Avoid repeating the same character 3 times in a row (like 'aaa').")
            break

    easy_patterns = ["123", "234", "345", "456", "567", "678", "789",
                     "abc", "bcd", "cde", "qwe", "asd"]
    for pattern in easy_patterns:
        if pattern in password.lower():
            score = score - 1
            tips.append("Avoid easy patterns like '123' or 'abc'.")
            break

    if score < 0:
        score = 0

    return score, tips


def get_rating(score):
    if score <= 2:
        return "WEAK"
    elif score <= 4:
        return "MEDIUM"
    elif score == 5:
        return "STRONG"
    else:
        return "VERY STRONG"


def make_strong_password(length=14):
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    new_password = ""
    for i in range(length):
        new_password = new_password + secrets.choice(all_chars)
    return new_password


def run_program():
    """The interactive part of the program. Kept in its own function
    so that check_password, get_rating, and make_strong_password can be
    imported and tested without this loop running automatically."""

    print("=== Password Strength Checker ===")
    print("Enter the app name and its password.")
    print("Type 'done' as the app name when you finish.\n")

    saved = {}

    while True:
        app = input("App name (or 'done'): ").strip()

        if app.lower() == "done":
            break

        if app == "":
            print("App name cannot be empty.\n")
            continue

        password = input("Password for " + app + ": ")

        if password == "":
            print("Password cannot be empty.\n")
            continue

        score, tips = check_password(password)

        print("\nStrength:", get_rating(score), "(" + str(score) + "/6)")

        if len(tips) == 0:
            print("Great password! Nothing to improve.")
        else:
            print("How to improve:")
            for tip in tips:
                print(" -", tip)
        print()

        saved[app] = password

    print("\n=== Reuse Check ===")

    if len(saved) == 0:
        print("No passwords entered.")
    else:
        used_in = {}

        for app in saved:
            pw = saved[app]
            if pw in used_in:
                used_in[pw].append(app)
            else:
                used_in[pw] = [app]

        found_reuse = False

        for pw in used_in:
            apps_list = used_in[pw]
            if len(apps_list) > 1:
                found_reuse = True
                print("\nSame password used in:", ", ".join(apps_list))
                print("If one app gets hacked, hackers can enter all of these!")
                print("Use a different password for each app. Suggestions:")
                for app in apps_list:
                    print("  ", app, "->", make_strong_password())

        if not found_reuse:
            print("Good job! All your passwords are unique.")

    print("\nStay safe online!")

if __name__ == "__main__":
    run_program()