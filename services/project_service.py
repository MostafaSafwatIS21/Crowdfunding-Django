from exceptions.base import ValidationException
from repositories.project_repository import ProjectRepository
from validators.project_validator import ProjectValidator
from models.project import Project

class ProjectService:
    def __init__(self, project_repo: ProjectRepository, project_validator: ProjectValidator):
        self.project_repo = project_repo
        self.project_validator = project_validator

    def create_project(self, data: dict, owner_id: int) -> Project:
        """Validate and create a new project."""
        validated_data = self.project_validator.validate_project_data(data)
        return self.project_repo.create(validated_data, owner_id)

    def get_all_projects(self) -> list[Project]:
        """Retrieve all projects."""
        return self.project_repo.get_all()

    def get_project(self, project_id: int) -> Project:
        """Retrieve a specific project by ID. Raises Exception if not found."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise Exception("Project not found.")
        return project

    def update_project(self, project_id: int, data: dict, current_user_id: int) -> Project:
        """Validate and update an existing project. Only the owner can update it."""
        project = self.get_project(project_id)
        
        if project.owner_id != current_user_id:
            raise Exception("Unauthorized: You can only edit your own projects.")

        validated_data = self.project_validator.validate_project_data(data)
        return self.project_repo.update(project, validated_data)

    def delete_project(self, project_id: int, current_user_id: int) -> bool:
        """Delete an existing project. Only the owner can delete it."""
        project = self.get_project(project_id)
        
        if project.owner_id != current_user_id:
            raise Exception("Unauthorized: You can only delete your own projects.")

        return self.project_repo.delete(project)

    def search_projects(self, start_date_str: str, end_date_str: str) -> list[Project]:
        """Validate search dates and return matching projects."""
        start_date, end_date = self.project_validator.validate_search_dates(start_date_str, end_date_str)
        return self.project_repo.search_by_dates(start_date, end_date)
