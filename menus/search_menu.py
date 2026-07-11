from services.project_service import ProjectService
from exceptions.base import ValidationException
from utils.console import get_input
from utils.formatter import print_header, print_project, print_validation_errors, print_error

class SearchMenu:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def handle_search(self):
        print_header("Search Projects")
        print("Leave date blank to skip filtering by that date.")
        
        try:
            start_date = get_input("Enter Start Date (YYYY-MM-DD): ", required=False)
            end_date = get_input("Enter End Date (YYYY-MM-DD): ", required=False)
            
            projects = self.project_service.search_projects(start_date, end_date)
            
            if not projects:
                print("\nNo projects found.")
                return
                
            for p in projects:
                print_project(p)
                
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
        except Exception as e:
            print_error(str(e))
