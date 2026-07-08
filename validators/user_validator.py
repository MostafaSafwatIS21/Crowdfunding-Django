import re
from exceptions.base import ValidationException
from repositories.user_repository import UserRepository

class UserValidator:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def is_valid_email_format(self, email: str) -> bool:
        """Validate if the email has a correct general format."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_regex, email))

    def is_valid_egyptian_phone(self, phone: str) -> bool:
        """Validate if phone matches standard Egyptian formats (010, 011, 012, 015 with 11 digits)."""
        phone_regex = r"^01[0125]\d{8}$"
        return bool(re.match(phone_regex, phone))

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
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors[field] = f"{label} is required."

        # 2. Email format & uniqueness
        email = data.get("email")
        if isinstance(email, str) and email.strip():
            email = email.strip()
            if not self.is_valid_email_format(email):
                errors["email"] = "Invalid email format."
            elif self.user_repo.exists(email):
                errors["email"] = "Email is already registered."

        # 3. Egyptian phone number validation
        phone = data.get("phone")
        if isinstance(phone, str) and phone.strip():
            phone = phone.strip()
            if not self.is_valid_egyptian_phone(phone):
                errors["phone"] = "Invalid Egyptian phone number. Must start with 010, 011, 012, or 015 and be exactly 11 digits."

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
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors[field] = f"{label} is required."

        # 2. Email format & uniqueness (excluding the current user)
        email = data.get("email")
        if isinstance(email, str) and email.strip():
            email = email.strip()
            if not self.is_valid_email_format(email):
                errors["email"] = "Invalid email format."
            elif self.user_repo.email_exists_excluding_user(email, current_user_id):
                errors["email"] = "Email is already registered by another user."

        # 3. Egyptian phone validation
        phone = data.get("phone")
        if isinstance(phone, str) and phone.strip():
            phone = phone.strip()
            if not self.is_valid_egyptian_phone(phone):
                errors["phone"] = "Invalid Egyptian phone number. Must start with 010, 011, 012, or 015 and be exactly 11 digits."

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
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors[field] = f"{label} is required."

        # 2. New password matching check
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            errors["confirm_password"] = "New passwords do not match."

        if errors:
            raise ValidationException("Password change validation error occurred", errors)
