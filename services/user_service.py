from models.user import User
from repositories.user_repository import UserRepository
from validators.user_validator import UserValidator
from utils.security import verify_password, hash_password
from exceptions.auth_exceptions import UserNotFoundException
from exceptions.base import ValidationException

class UserService:
    def __init__(self, user_repo: UserRepository, user_validator: UserValidator):
        self.user_repo = user_repo
        self.user_validator = user_validator

    def get_profile(self, user_id: int) -> User:
        """Retrieve user profile by user_id."""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))
        return user

    def update_profile(self, user_id: int, update_data: dict) -> User:
        """Validate and apply updates to user profile details."""
        # 1. Fetch user
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))

        # 2. Validate update data
        self.user_validator.validate_profile_update(update_data, user_id)

        # 3. Apply changes
        user.first_name = update_data.get("first_name", "").strip()
        user.last_name = update_data.get("last_name", "").strip()
        user.email = update_data.get("email", "").strip().lower()
        user.phone = update_data.get("phone", "").strip()

        # 4. Save to database
        return self.user_repo.update(user)

    def change_password(self, user_id: int, password_data: dict) -> User:
        """Validate and change user's password."""
        # 1. Fetch user
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(str(user_id))

        # 2. Validate password change inputs (new matching checks, etc.)
        self.user_validator.validate_password_change(password_data)

        # 3. Verify current password matches
        old_password = password_data.get("old_password")
        if not verify_password(old_password, user.password):
            raise ValidationException("Password verification failed", {
                "old_password": "Old password is incorrect."
            })

        # 4. Hash and save the new password
        new_password = password_data.get("new_password")
        user.password = hash_password(new_password)

        # 5. Persist updates
        return self.user_repo.update(user)
