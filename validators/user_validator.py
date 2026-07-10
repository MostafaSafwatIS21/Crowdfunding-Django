from exceptions.base import ValidationException
from repositories.user_repository import UserRepository
from validators.common import (
    validate_email_format,
    validate_egyptian_phone,
    validate_required_string
)

class UserValidator:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def validate_registration(self, data: dict) -> None:
        """Validate registration data and raise ValidationException if invalid."""
        errors = {}

        # 1. Required fields check
        required_fields = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
            "password": "Password",
            "confirm_password": "Confirm password",
            "phone": "Phone number"
        }
        
        for field, label in required_fields.items():
            try:
                validate_required_string(data.get(field), label)
            except ValidationException as e:
                errors[field] = e.errors[label]

        # 2. Email format & uniqueness
        if "email" not in errors and data.get("email"):
            try:
                email = validate_email_format(data.get("email"))
                if self.user_repo.exists(email):
                    errors["email"] = "Email is already registered."
            except ValidationException as e:
                errors["email"] = e.errors["email"]

        # 3. Egyptian phone number validation
        if "phone" not in errors and data.get("phone"):
            try:
                validate_egyptian_phone(data.get("phone"))
            except ValidationException as e:
                errors["phone"] = e.errors["phone"]

        # 4. Password matching check
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if errors:
            raise ValidationException("Validation error occurred", errors)

    def validate_profile_update(self, data: dict, current_user_id: int) -> None:
        """Validate profile update data and raise ValidationException if invalid."""
        errors = {}

        # 1. Required fields check
        required_fields = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
            "phone": "Phone number"
        }
        
        for field, label in required_fields.items():
            try:
                validate_required_string(data.get(field), label)
            except ValidationException as e:
                errors[field] = e.errors[label]

        # 2. Email format & uniqueness (excluding the current user)
        if "email" not in errors and data.get("email"):
            try:
                email = validate_email_format(data.get("email"))
                if self.user_repo.email_exists_excluding_user(email, current_user_id):
                    errors["email"] = "Email is already registered by another user."
            except ValidationException as e:
                errors["email"] = e.errors["email"]

        # 3. Egyptian phone validation
        if "phone" not in errors and data.get("phone"):
            try:
                validate_egyptian_phone(data.get("phone"))
            except ValidationException as e:
                errors["phone"] = e.errors["phone"]

        if errors:
            raise ValidationException("Profile validation error occurred", errors)

    def validate_password_change(self, data: dict) -> None:
        """Validate password change inputs and raise ValidationException if invalid."""
        errors = {}

        # 1. Required fields check
        required_fields = {
            "old_password": "Old password",
            "new_password": "New password",
            "confirm_password": "Confirm new password"
        }

        for field, label in required_fields.items():
            try:
                validate_required_string(data.get(field), label)
            except ValidationException as e:
                errors[field] = e.errors[label]

        # 2. New password matching check
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            errors["confirm_password"] = "New passwords do not match."

        if errors:
            raise ValidationException("Password change validation error occurred", errors)
