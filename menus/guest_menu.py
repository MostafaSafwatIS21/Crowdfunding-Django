from services.authentication_service import AuthenticationService
from exceptions.base import ValidationException
from exceptions.auth_exceptions import InvalidCredentialsException
from utils.console import get_input, get_password
from utils.formatter import print_header, print_success, print_error, print_validation_errors

class GuestMenu:
    def __init__(self, auth_service: AuthenticationService):
        self.auth_service = auth_service
        self.logged_in_user = None

    def display(self):
        while True:
            print_header("Guest Menu")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            try:
                choice = get_input("Select an option (1-3): ", required=True)
                
                if choice == "1":
                    self._handle_register()
                elif choice == "2":
                    user = self._handle_login()
                    if user:
                        self.logged_in_user = user
                        return  # Exit guest menu to go to user menu
                elif choice == "3":
                    print("\nExiting. Goodbye!")
                    return
                else:
                    print_error("Invalid menu option. Please choose a valid option (1-3).")
            except InterruptedError:
                # User hit Ctrl+C during input, we just loop back to menu
                pass

    def _handle_register(self):
        print_header("Create a New Account")
        
        try:
            data = {
                "first_name": get_input("First Name: "),
                "last_name": get_input("Last Name: "),
                "email": get_input("Email: "),
                "phone": get_input("Egyptian Phone Number: "),
                "password": get_password("Password: "),
                "confirm_password": get_password("Confirm Password: ")
            }
            
            self.auth_service.register(data)
            print_success("Registration successful! You can now log in.")
            
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
            
    def _handle_login(self):
        print_header("Account Login")
        
        try:
            email = get_input("Email: ")
            password = get_password("Password: ")
            
            user = self.auth_service.login(email, password)
            print_success(f"Login successful! Welcome, {user.first_name}!")
            return user
        except InvalidCredentialsException:
            print_error("Invalid email or password.")
            return None
        except ValidationException as e:
            print_validation_errors(e.errors)
            return None
        except InterruptedError:
            return None
