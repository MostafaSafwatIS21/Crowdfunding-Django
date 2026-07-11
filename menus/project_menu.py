from services.project_service import ProjectService
from exceptions.base import ValidationException
from utils.console import get_input, prompt_confirmation
from utils.formatter import print_header, print_success, print_error, print_project, print_validation_errors

class ProjectMenu:
    def __init__(self, project_service: ProjectService, user_id: int):
        self.project_service = project_service
        self.user_id = user_id

    def handle_create_project(self):
        print_header("Create a New Project")
        try:
            data = {
                "title": get_input("Title: "),
                "details": get_input("Details: "),
                "total_target": get_input("Target Amount (EGP): "),
                "start_date": get_input("Start Date (YYYY-MM-DD): "),
                "end_date": get_input("End Date (YYYY-MM-DD): ")
            }
            
            self.project_service.create_project(data, self.user_id)
            print_success("Project created successfully.")
            
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
        except Exception as e:
            print_error(str(e))

    def handle_view_projects(self):
        print_header("All Projects")
        try:
            projects = self.project_service.get_all_projects()
            if not projects:
                print("No projects found.")
                return
                
            for project in projects:
                print_project(project)
        except Exception as e:
            print_error(f"Failed to fetch projects: {e}")

    def handle_edit_project(self):
        print_header("Edit My Project")
        try:
            # Quick view of own projects (optional improvement, but just ask ID for now)
            project_id_str = get_input("Enter Project ID: ")
            if not project_id_str.isdigit():
                print_error("Project ID must be a number.")
                return
            project_id = int(project_id_str)
            
            project = self.project_service.get_project(project_id)
            
            print("Leave fields blank to keep current values.")
            title = get_input(f"Title [{project.title}]: ", required=False) or project.title
            details = get_input(f"Details [{project.details}]: ", required=False) or project.details
            total_target = get_input(f"Target Amount [{project.total_target}]: ", required=False) or project.total_target
            start_date = get_input(f"Start Date [{project.start_date}]: ", required=False) or str(project.start_date)
            end_date = get_input(f"End Date [{project.end_date}]: ", required=False) or str(project.end_date)
            
            data = {
                "title": title,
                "details": details,
                "total_target": total_target,
                "start_date": start_date,
                "end_date": end_date
            }
            
            self.project_service.update_project(project_id, self.user_id, data)
            print_success("Project updated successfully.")
            
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
        except Exception as e:
            print_error(str(e))

    def handle_delete_project(self):
        print_header("Delete My Project")
        try:
            project_id_str = get_input("Enter Project ID: ")
            if not project_id_str.isdigit():
                print_error("Project ID must be a number.")
                return
            project_id = int(project_id_str)
            
            if prompt_confirmation("Are you sure you want to delete this project?"):
                self.project_service.delete_project(project_id, self.user_id)
                print_success("Project deleted successfully.")
            
        except ValidationException as e:
            print_validation_errors(e.errors)
        except InterruptedError:
            pass
        except Exception as e:
            print_error(str(e))
