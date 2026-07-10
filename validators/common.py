import re
from datetime import datetime, date
from typing import Any
from exceptions.base import ValidationException

def validate_required_string(value: Any, field_name: str) -> str:
    """Validate that the given value is a non-empty string."""
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationException("Validation Error", {field_name: f"{field_name} is required."})
    return str(value).strip()

def validate_positive_number(value: Any, field_name: str) -> float:
    """Validate that the given value is a positive number."""
    try:
        num = float(value)
        if num <= 0:
            raise ValidationException("Validation Error", {field_name: f"{field_name} must be greater than zero."})
        return num
    except (ValueError, TypeError):
        raise ValidationException("Validation Error", {field_name: f"{field_name} must be a valid number."})

def validate_email_format(email: str) -> str:
    """Validate if the email has a correct general format."""
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    email = validate_required_string(email, "Email")
    if not re.match(email_regex, email):
        raise ValidationException("Validation Error", {"email": "Invalid email format."})
    return email

def validate_egyptian_phone(phone: str) -> str:
    """Validate if phone matches standard Egyptian formats."""
    phone_regex = r"^01[0125]\d{8}$"
    phone = validate_required_string(phone, "Phone number")
    if not re.match(phone_regex, phone):
        raise ValidationException("Validation Error", {"phone": "Invalid Egyptian phone number. Must start with 010, 011, 012, or 015 and be exactly 11 digits."})
    return phone

def validate_date_format(date_str: str, field_name: str, fmt: str = "%Y-%m-%d") -> date:
    """Validate that a string matches a specific date format."""
    date_str = validate_required_string(date_str, field_name)
    try:
        return datetime.strptime(date_str, fmt).date()
    except ValueError:
        raise ValidationException("Validation Error", {field_name: f"Invalid date format for {field_name}. Expected {fmt}."})

def validate_date_range(start_date: date, end_date: date, start_field: str = "start_date", end_field: str = "end_date") -> None:
    """Validate that the end date is strictly after the start date."""
    if end_date <= start_date:
        raise ValidationException("Validation Error", {end_field: f"{end_field.replace('_', ' ').capitalize()} must be strictly after {start_field.replace('_', ' ').capitalize()}."})
