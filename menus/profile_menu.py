from services.user_service import UserService
from exceptions.base import ValidationException
from utils.console import get_input, get_password
from utils.formatter import print_header, print_success, print_profile, print_validation_errors

class ProfileMenu:
    def __init__(self, user_service: UserService, user_id: int):
        self.user_service = user_service
        self.user_id = user_id

    def handle_view_profile(self):
        try:
            user = self.user_service.get_profile(self.user_id)
            print_profile(user)
        except Exception as e:
            print(f"\n[Error] Could not fetch profile: {e}")
            
    def handle_update_profile(self):
        print_header("Update Profile Details")
        try:
            user = self.user_service.get_profile(self.user_id)
            
            # Show current values and get new ones
            first_name = get_input(f"First Name [{user.first_name}]: ", required=False) or user.first_name
            last_name = get_input(f"Last Name [{user.last_name}]: ", required=False) or user.last_name
            email = get_input(f"Email [{user.email}]: ", required=False) or user.email
            phone = get_input(f"Phone [{user.phone}]: ", required=False) or user.phone
            
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone
            }
            
            self.user_service.update_profile(self.user_id, data)
            print_success("Profile updated successfully!")
            
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
        except Exception as e:
            print(f"\n[Error] {e}")

    def handle_change_password(self):
        print_header("Change Password")
        try:
            data = {
                "old_password": get_password("Current Password: "),
                "new_password": get_password("New Password: "),
                "confirm_password": get_password("Confirm New Password: ")
            }
            
            self.user_service.change_password(self.user_id, data)
            print_success("Password changed successfully!")
            
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
        except Exception as e:
            print(f"\n[Error] {e}")
