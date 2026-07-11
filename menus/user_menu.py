from services.user_service import UserService
from services.project_service import ProjectService
from models.user import User
from utils.console import get_input
from utils.formatter import print_header, print_error
from menus.profile_menu import ProfileMenu
from menus.project_menu import ProjectMenu
from menus.search_menu import SearchMenu

class UserMenu:
    def __init__(self, user: User, user_service: UserService, project_service: ProjectService):
        self.user = user
        self.user_service = user_service
        self.project_service = project_service
        self.profile_menu = ProfileMenu(user_service, user.id)
        self.project_menu = ProjectMenu(project_service, user.id)
        self.search_menu = SearchMenu(project_service)

    def display(self):
        while True:
            print_header(f"User Dashboard - Welcome {self.user.first_name}")
            print("1. View Profile")
            print("2. Update Profile")
            print("3. Create Project")
            print("4. View Projects")
            print("5. Edit My Project")
            print("6. Delete My Project")
            print("7. Search Projects")
            print("8. Logout")
            
            try:
                choice = get_input("Select an option (1-8): ", required=True)
                
                if choice == "1":
                    self.profile_menu.handle_view_profile()
                elif choice == "2":
                    self.profile_menu.handle_update_profile()
                elif choice == "3":
                    self.project_menu.handle_create_project()
                elif choice == "4":
                    self.project_menu.handle_view_projects()
                elif choice == "5":
                    self.project_menu.handle_edit_project()
                elif choice == "6":
                    self.project_menu.handle_delete_project()
                elif choice == "7":
                    self.search_menu.handle_search()
                elif choice == "8":
                    print("\nLogging out...")
                    return  # Return to main menu which will send to guest menu
                else:
                    print_error("Invalid menu option. Please choose a valid option (1-8).")
            except InterruptedError:
                pass
