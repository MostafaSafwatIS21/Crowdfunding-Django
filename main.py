import sys
from config.settings import logger
from database.connection import SessionLocal
from repositories.user_repository import UserRepository
from validators.user_validator import UserValidator
from services.auth_service import AuthService
from menus.main_menu import MainMenu

def main():
    logger.info("Starting Crowdfunding Console Application...")
    
    # 1. Initialize DB Session
    db = SessionLocal()
    
    try:
        # 2. Instantiate repository, validator, and service layers
        user_repo = UserRepository(db)
        user_validator = UserValidator(user_repo)
        auth_service = AuthService(user_repo, user_validator)
        
        # 3. Launch main menu CLI
        menu = MainMenu(auth_service)
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error during execution: {e}", exc_info=True)
        print(f"\n[Fatal Error] The application crashed: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
