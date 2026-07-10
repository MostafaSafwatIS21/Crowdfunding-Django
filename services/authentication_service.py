from models.user import User
from repositories.user_repository import UserRepository
from validators.user_validator import UserValidator
from utils.security import hash_password, verify_password
from exceptions.auth_exceptions import InvalidCredentialsException

class AuthenticationService:
    def __init__(self, user_repo: UserRepository, user_validator: UserValidator):
        self.user_repo = user_repo
        self.user_validator = user_validator

    def register(self, registration_data: dict) -> User:
        """Validate, hash password, and register a new user."""
        # 1. Validate data
        self.user_validator.validate_registration(registration_data)

        # 2. Extract values and clean
        first_name = registration_data.get("first_name", "").strip()
        last_name = registration_data.get("last_name", "").strip()
        email = registration_data.get("email", "").strip().lower()  # Normalize email to lower case
        password = registration_data.get("password")
        phone = registration_data.get("phone", "").strip()

        # 3. Hash password
        hashed_password = hash_password(password)

        # 4. Create User instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            phone=phone
        )

        # 5. Persist to database
        return self.user_repo.create(new_user)

    def login(self, email: str, password: str) -> User:
        """Authenticate user by email and password, returning User if successful."""
        email_clean = email.strip().lower()
        
        # 1. Retrieve user
        user = self.user_repo.get_by_email(email_clean)
        if not user:
            raise InvalidCredentialsException()

        # 2. Verify password
        if not verify_password(password, user.password):
            raise InvalidCredentialsException()

        return user
