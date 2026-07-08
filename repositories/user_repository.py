from sqlalchemy.orm import Session
from models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        """Persist a new User model to the database."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address."""
        # Case insensitive email check is often preferred, but standard filter is fine.
        # Let's keep it exact as email is unique.
        return self.db.query(User).filter(User.email == email).first()

    def exists(self, email: str) -> bool:
        """Check if a user exists with the given email address."""
        return self.db.query(User.id).filter(User.email == email).first() is not None
