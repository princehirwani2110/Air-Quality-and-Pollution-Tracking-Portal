"""Entry point for the Air Quality CLI.

This file now delegates admin and citizen functionality to separate modules:
- admin.py
- citizen.py

Run with: python main.py
"""

import sys
import utils
import admin
import citizen


def main_menu():
    utils.ensure_sample_data()
    print("=== Air Quality & Pollution Tracking Portal ===")
    while True:
        print("Main Menu:\n1.Admin Login\n2.Citizen Login\n3.Register as New Citizen\n4.Exit")
        ch = input("Choice: ").strip()
        if ch == "1":
            if admin.admin_login():
                admin.admin_menu()
        elif ch == "2":
            # citizen_login prompts for ID and opens menu when found
            citizen.citizen_login()
        elif ch == "3":
            citizen.register_citizen()
        elif ch == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
