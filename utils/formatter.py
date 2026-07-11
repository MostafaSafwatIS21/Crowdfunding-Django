def print_header(title: str):
    """Print a standardized menu header."""
    print(f"\n{'-' * 41}")
    print(title)
    print(f"{'-' * 41}")

def print_separator():
    """Print a standard separator line."""
    print(f"====================================")

def print_success(message: str):
    """Print a success message."""
    print(f"\n[Success] {message}")

def print_error(message: str):
    """Print an error message."""
    print(f"\n[Error] {message}")

def print_validation_errors(errors: dict):
    """Print a list of validation errors beautifully."""
    print_error("Validation failed:")
    for field, err in errors.items():
        print(f"  - {field.replace('_', ' ').capitalize()}: {err}")

def print_project(project):
    """Print a single project formatted with separators."""
    print_separator()
    print(f"Project ID: {project.id}")
    print(f"Title: {project.title}")
    print(f"Owner ID: {project.owner_id}")
    print(f"Target: {project.total_target} EGP")
    print(f"Start: {project.start_date}")
    print(f"End: {project.end_date}")
    print_separator()

def print_profile(user):
    """Print a user profile."""
    print_separator()
    print("User Profile Details")
    print_separator()
    print(f"Full Name: {user.first_name} {user.last_name}")
    print(f"Email: {user.email}")
    print(f"Phone: {user.phone}")
    print(f"Registration Date: {user.created_at.strftime('%Y-%m-%d')}")
    print_separator()
