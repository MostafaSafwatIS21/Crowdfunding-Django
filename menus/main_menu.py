import sys
import getpass
from services.authentication_service import AuthenticationService
from services.user_service import UserService
from exceptions.base import ValidationException
from exceptions.auth_exceptions import InvalidCredentialsException

from menus.project_menu import ProjectMenu

class MainMenu:
    def __init__(self, auth_service: AuthenticationService, user_service: UserService, project_service):
        self.auth_service = auth_service
        self.user_service = user_service
        self.project_service = project_service
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
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Change Password")
        print("4. Manage Projects")
        print("5. Logout")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            self.handle_view_profile()
        elif choice == "2":
            self.handle_update_profile()
        elif choice == "3":
            self.handle_change_password()
        elif choice == "4":
            project_menu = ProjectMenu(self.project_service, self.logged_in_user)
            project_menu.show()
        elif choice == "5":
            print(f"\nLogged out successfully from account: {self.logged_in_user.email}")
            self.logged_in_user = None
        elif choice == "6":
            print("\nThank you for using the Crowdfunding Platform. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Error] Invalid choice. Please select a number between 1 and 6.")

    def handle_registration(self):
        print("\n--- Create a New Account ---")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
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

    def handle_view_profile(self):
        print("\n--- User Profile Details ---")
        try:
            user = self.user_service.get_profile(self.logged_in_user.id)
            self.logged_in_user = user
            print(f"  First Name:  {user.first_name}")
            print(f"  Last Name:   {user.last_name}")
            print(f"  Email:       {user.email}")
            print(f"  Phone:       {user.phone}")
            print(f"  Joined On:   {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"\n[Error] Failed to fetch profile details: {e}")

    def handle_update_profile(self):
        print("\n--- Update Profile Details ---")
        try:
            user = self.user_service.get_profile(self.logged_in_user.id)
            self.logged_in_user = user
            
            first_name = input(f"First Name [{user.first_name}]: ").strip() or user.first_name
            last_name = input(f"Last Name [{user.last_name}]: ").strip() or user.last_name
            email = input(f"Email [{user.email}]: ").strip() or user.email
            phone = input(f"Phone [{user.phone}]: ").strip() or user.phone

            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone
            }

            confirm = input("\nAre you sure you want to save these changes? (y/N): ").strip().lower()
            if confirm not in ("y", "yes"):
                print("\n[Cancelled] Profile update cancelled.")
                return

            updated_user = self.user_service.update_profile(user.id, data)
            self.logged_in_user = updated_user
            print("\n[Success] Profile updated successfully!")
        except ValidationException as e:
            print("\n[Error] Profile update failed due to validation issues:")
            for field, error in e.errors.items():
                print(f"  - {field.replace('_', ' ').capitalize()}: {error}")
        except Exception as e:
            print(f"\n[Error] Failed to update profile: {e}")

    def handle_change_password(self):
        print("\n--- Change Password ---")
        try:
            old_password = getpass.getpass("Current Password: ")
            new_password = getpass.getpass("New Password: ")
            confirm_password = getpass.getpass("Confirm New Password: ")

            data = {
                "old_password": old_password,
                "new_password": new_password,
                "confirm_password": confirm_password
            }

            confirm = input("\nAre you sure you want to change your password? (y/N): ").strip().lower()
            if confirm not in ("y", "yes"):
                print("\n[Cancelled] Password change cancelled.")
                return

            self.user_service.change_password(self.logged_in_user.id, data)
            print("\n[Success] Password changed successfully!")
        except ValidationException as e:
            print("\n[Error] Password change failed due to validation issues:")
            for field, error in e.errors.items():
                print(f"  - {field.replace('_', ' ').capitalize()}: {error}")
        except Exception as e:
            print(f"\n[Error] Failed to change password: {e}")
