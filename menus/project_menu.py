from services.project_service import ProjectService
from exceptions.base import ValidationException

class ProjectMenu:
    def __init__(self, project_service: ProjectService, logged_in_user):
        self.project_service = project_service
        self.logged_in_user = logged_in_user

    def show(self):
        while True:
            print(f"\n--- Manage Projects ---")
            print("1. View all projects")
            print("2. Search projects by date")
            print("3. View project details")
            print("4. Create a new project")
            print("5. Edit your project")
            print("6. Delete your project")
            print("7. Return to Main Menu")
            
            choice = input("Select an option (1-7): ").strip()
            
            if choice == "1":
                self.handle_view_all()
            elif choice == "2":
                self.handle_search()
            elif choice == "3":
                self.handle_view_details()
            elif choice == "4":
                self.handle_create()
            elif choice == "5":
                self.handle_edit()
            elif choice == "6":
                self.handle_delete()
            elif choice == "7":
                break
            else:
                print("\n[Error] Invalid choice.")

    def handle_view_all(self):
        print("\n--- All Projects ---")
        projects = self.project_service.get_all_projects()
        if not projects:
            print("No projects found.")
            return
        for p in projects:
            print(f"[{p.id}] {p.title} - Target: {p.total_target} - Dates: {p.start_date} to {p.end_date}")

    def handle_search(self):
        print("\n--- Search Projects ---")
        print("Leave blank to skip filtering by that date.")
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        
        try:
            projects = self.project_service.search_projects(start_date, end_date)
            if not projects:
                print("No projects found matching the criteria.")
                return
            for p in projects:
                print(f"[{p.id}] {p.title} - Target: {p.total_target} - Dates: {p.start_date} to {p.end_date}")
        except ValidationException as e:
            print("\n[Error] Validation failed:")
            for field, err in e.errors.items():
                print(f"  - {field.replace('_', ' ').capitalize()}: {err}")

    def handle_view_details(self):
        print("\n--- Project Details ---")
        try:
            project_id = int(input("Enter Project ID: ").strip())
            p = self.project_service.get_project(project_id)
            print(f"\nTitle: {p.title}")
            print(f"Details: {p.details}")
            print(f"Target: {p.total_target}")
            print(f"Start Date: {p.start_date}")
            print(f"End Date: {p.end_date}")
            print(f"Owner ID: {p.owner_id}")
            print(f"Created At: {p.created_at}")
        except ValueError:
            print("\n[Error] Invalid ID format.")
        except Exception as e:
            print(f"\n[Error] {str(e)}")

    def handle_create(self):
        print("\n--- Create New Project ---")
        title = input("Title: ").strip()
        details = input("Details: ").strip()
        total_target = input("Total Target Amount: ").strip()
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()

        data = {
            "title": title,
            "details": details,
            "total_target": total_target,
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            project = self.project_service.create_project(data, self.logged_in_user.id)
            print(f"\n[Success] Project '{project.title}' created successfully!")
        except ValidationException as e:
            print("\n[Error] Validation failed:")
            for field, err in e.errors.items():
                print(f"  - {field.replace('_', ' ').capitalize()}: {err}")
        except Exception as e:
            print(f"\n[Error] An unexpected error occurred: {e}")

    def handle_edit(self):
        print("\n--- Edit Project ---")
        try:
            project_id = int(input("Enter Project ID to edit: ").strip())
            # Fetch to show current values
            p = self.project_service.get_project(project_id)
            if p.owner_id != self.logged_in_user.id:
                print("\n[Error] Unauthorized: You can only edit your own projects.")
                return

            print("Leave blank to keep current value.")
            title = input(f"Title [{p.title}]: ").strip() or p.title
            details = input(f"Details [{p.details}]: ").strip() or p.details
            total_target = input(f"Target [{p.total_target}]: ").strip() or str(p.total_target)
            start_date = input(f"Start Date [{p.start_date}]: ").strip() or str(p.start_date)
            end_date = input(f"End Date [{p.end_date}]: ").strip() or str(p.end_date)

            data = {
                "title": title,
                "details": details,
                "total_target": total_target,
                "start_date": start_date,
                "end_date": end_date
            }

            self.project_service.update_project(project_id, data, self.logged_in_user.id)
            print("\n[Success] Project updated successfully!")

        except ValueError:
            print("\n[Error] Invalid ID format.")
        except ValidationException as e:
            print("\n[Error] Validation failed:")
            for field, err in e.errors.items():
                print(f"  - {field.replace('_', ' ').capitalize()}: {err}")
        except Exception as e:
            print(f"\n[Error] {str(e)}")

    def handle_delete(self):
        print("\n--- Delete Project ---")
        try:
            project_id = int(input("Enter Project ID to delete: ").strip())
            
            confirm = input(f"Are you sure you want to delete project {project_id}? (y/N): ").strip().lower()
            if confirm not in ("y", "yes"):
                print("\n[Cancelled] Deletion cancelled.")
                return
                
            self.project_service.delete_project(project_id, self.logged_in_user.id)
            print("\n[Success] Project deleted successfully!")
        except ValueError:
            print("\n[Error] Invalid ID format.")
        except Exception as e:
            print(f"\n[Error] {str(e)}")
