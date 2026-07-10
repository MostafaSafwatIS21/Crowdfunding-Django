from exceptions.base import ValidationException
from validators.common import (
    validate_required_string,
    validate_positive_number,
    validate_date_format,
    validate_date_range
)

class ProjectValidator:
    def validate_project_data(self, data: dict) -> dict:
        """Validate project creation/update data. Returns validated and parsed data."""
        errors = {}
        validated_data = {}

        # 1. Required string fields
        for field, label in [("title", "Title"), ("details", "Details")]:
            try:
                validated_data[field] = validate_required_string(data.get(field), label)
            except ValidationException as e:
                errors[field] = e.errors[label]

        # 2. Target validation (positive number)
        try:
            validated_data["total_target"] = validate_positive_number(data.get("total_target"), "Total target")
        except ValidationException as e:
            errors["total_target"] = e.errors["Total target"]

        # 3. Dates validation
        start_date = None
        end_date = None
        
        try:
            start_date = validate_date_format(data.get("start_date"), "Start date")
            validated_data["start_date"] = start_date
        except ValidationException as e:
            errors["start_date"] = e.errors["Start date"]

        try:
            end_date = validate_date_format(data.get("end_date"), "End date")
            validated_data["end_date"] = end_date
        except ValidationException as e:
            errors["end_date"] = e.errors["End date"]

        # 4. Date range validation
        if start_date and end_date:
            try:
                validate_date_range(start_date, end_date)
            except ValidationException as e:
                errors["end_date"] = e.errors["end_date"]

        if errors:
            raise ValidationException("Project validation error occurred", errors)
            
        return validated_data

    def validate_search_dates(self, start_date_str: str, end_date_str: str) -> tuple:
        """Validate dates for searching. Returns parsed dates as a tuple. Dates can be optional."""
        errors = {}
        start_date = None
        end_date = None

        if not start_date_str and not end_date_str:
            raise ValidationException("Search error", {"dates": "Please provide at least a start date or an end date to search."})

        if start_date_str:
            try:
                start_date = validate_date_format(start_date_str, "Start date")
            except ValidationException as e:
                errors["start_date"] = e.errors["Start date"]

        if end_date_str:
            try:
                end_date = validate_date_format(end_date_str, "End date")
            except ValidationException as e:
                errors["end_date"] = e.errors["End date"]

        if start_date and end_date:
            try:
                validate_date_range(start_date, end_date)
            except ValidationException as e:
                errors["end_date"] = e.errors["end_date"]

        if errors:
            raise ValidationException("Search dates validation error", errors)

        return start_date, end_date
