from sqlalchemy.orm import Session
from models.project import Project
from datetime import date

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_data: dict, owner_id: int) -> Project:
        """Create a new project in the database."""
        project = Project(**project_data, owner_id=owner_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def find_by_id(self, project_id: int) -> Project | None:
        """Retrieve a project by its ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def find_all(self) -> list[Project]:
        """Retrieve all projects."""
        return self.db.query(Project).all()

    def update(self, project: Project, project_data: dict) -> Project:
        """Update an existing project."""
        for key, value in project_data.items():
            setattr(project, key, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> bool:
        """Delete a project."""
        self.db.delete(project)
        self.db.commit()
        return True

    def search_by_dates(self, start_date: date | None, end_date: date | None) -> list[Project]:
        """Search projects. Filters by start_date and/or end_date if provided."""
        query = self.db.query(Project)
        if start_date:
            query = query.filter(Project.start_date >= start_date)
        if end_date:
            query = query.filter(Project.end_date <= end_date)
        return query.all()
