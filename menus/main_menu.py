import sys
import getpass
from services.auth_service import AuthService
from exceptions.base import ValidationException
from exceptions.auth_exceptions import InvalidCredentialsException

class MainMenu:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.logged_in_user = None

    def run(self):
        """Run the main CLI loop."""
        print("=" * 50)
        print("Welcome to the Crowdfunding Platform Console Application!")
        print("=" * 50)

        while True:
            if self.logged_in_user:
                self.show_logged_in_menu()
            else:
                self.show_visitor_menu()

    def show_visitor_menu(self):
        print("\n--- Main Menu ---")
        print("1. Register a new account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            self.handle_registration()
        elif choice == "2":
            self.handle_login()
        elif choice == "3":
            print("\nThank you for using the Crowdfunding Platform. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Error] Invalid choice. Please choose a number between 1 and 3.")

    def show_logged_in_menu(self):
        print(f"\n--- Logged In: Welcome {self.logged_in_user.first_name} {self.logged_in_user.last_name} ---")
        print("1. Logout")
        print("2. Exit")
        
        choice = input("Select an option (1-2): ").strip()
        
        if choice == "1":
            print(f"\nLogged out successfully from account: {self.logged_in_user.email}")
            self.logged_in_user = None
        elif choice == "2":
            print("\nThank you for using the Crowdfunding Platform. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Error] Invalid choice. Please select 1 or 2.")

    def handle_registration(self):
        print("\n--- Create a New Account ---")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
        
        # Using getpass if possible, or standard input with clear visual feedback
        # getpass hides the typed password which is standard/secure.
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        phone = input("Egyptian Phone Number (starts with 010/011/012/015): ").strip()

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "phone": phone
        }

        try:
            user = self.auth_service.register(data)
            print("\n[Success] Registration successful! You can now log in.")
            print(f"Details: {user.first_name} {user.last_name} ({user.email})")
        except ValidationException as e:
            print("\n[Error] Registration failed due to validation issues:")
            for field, error in e.errors.items():
                print(f"  - {field.replace('_', ' ').capitalize()}: {error}")
        except Exception as e:
            print(f"\n[Error] An unexpected error occurred: {e}")

    def handle_login(self):
        print("\n--- Account Login ---")
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")

        try:
            user = self.auth_service.login(email, password)
            self.logged_in_user = user
            print(f"\n[Success] Login successful! Welcome back, {user.first_name}!")
        except InvalidCredentialsException as e:
            print(f"\n[Error] {e.message}")
        except Exception as e:
            print(f"\n[Error] An unexpected error occurred: {e}")
