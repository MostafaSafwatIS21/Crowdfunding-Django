import re
from exceptions.base import ValidationException
from repositories.user_repository import UserRepository

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
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors[field] = f"{label} is required."

        # 2. Email format & uniqueness
        email = data.get("email")
        if isinstance(email, str) and email.strip():
            email = email.strip()
            # Basic email format regex
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, email):
                errors["email"] = "Invalid email format."
            elif self.user_repo.exists(email):
                errors["email"] = "Email is already registered."

        # 3. Egyptian phone number validation
        # Must start with 010, 011, 012, or 015 and be exactly 11 digits.
        phone = data.get("phone")
        if isinstance(phone, str) and phone.strip():
            phone = phone.strip()
            phone_regex = r"^01[0125]\d{8}$"
            if not re.match(phone_regex, phone):
                errors["phone"] = "Invalid Egyptian phone number. Must start with 010, 011, 012, or 015 and be exactly 11 digits."

        # 4. Password matching check
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        if errors:
            raise ValidationException("Validation error occurred", errors)
