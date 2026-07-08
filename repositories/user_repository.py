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

    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by their ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def email_exists_excluding_user(self, email: str, user_id: int) -> bool:
        """Check if another user exists with the given email address, excluding the specified user_id."""
        return self.db.query(User.id).filter(User.email == email, User.id != user_id).first() is not None

    def update_user(self, user: User) -> User:
        """Commit changes to a User model and return it."""
        self.db.commit()
        self.db.refresh(user)
        return user

