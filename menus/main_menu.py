from services.authentication_service import AuthenticationService
from services.user_service import UserService
from services.project_service import ProjectService
from menus.guest_menu import GuestMenu
from menus.user_menu import UserMenu

class MainMenu:
    def __init__(
        self,
        auth_service: AuthenticationService,
        user_service: UserService,
        project_service: ProjectService
    ):
        self.auth_service = auth_service
        self.user_service = user_service
        self.project_service = project_service

    def run(self):
        """Entry point for the console application."""
        print("=========================================")
        print("      Crowdfunding Console System")
        print("=========================================")
        print("Welcome!")
        print("Choose an option.")
        print("-----------------------------------------")
        
        while True:
            # We start in the GuestMenu
            guest_menu = GuestMenu(self.auth_service)
            guest_menu.display()
            
            # If guest_menu.display() returns, it means the user either chose Exit or they logged in
            if guest_menu.logged_in_user:
                # User logged in, transition to UserMenu
                user_menu = UserMenu(
                    user=guest_menu.logged_in_user,
                    user_service=self.user_service,
                    project_service=self.project_service
                )
                user_menu.display()
                # If user_menu.display() returns, it means the user logged out
            else:
                # User chose exit from GuestMenu
                break
