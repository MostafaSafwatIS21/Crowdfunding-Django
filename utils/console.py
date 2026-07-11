import getpass

def get_input(prompt: str, required: bool = True) -> str:
    """Safely get string input from the user."""
    while True:
        try:
            value = input(prompt).strip()
            if required and not value:
                print("\n[Error] This field is required. Please try again.")
                continue
            return value
        except (KeyboardInterrupt, EOFError):
            print("\n\nInput cancelled. Returning to menu...")
            raise InterruptedError("User cancelled input.")

def get_password(prompt: str = "Password: ", required: bool = True) -> str:
    """Safely get hidden password input from the user."""
    while True:
        try:
            value = getpass.getpass(prompt).strip()
            if required and not value:
                print("\n[Error] Password is required. Please try again.")
                continue
            return value
        except (KeyboardInterrupt, EOFError):
            print("\n\nInput cancelled. Returning to menu...")
            raise InterruptedError("User cancelled input.")

def prompt_confirmation(prompt: str = "Are you sure?") -> bool:
    """Ask the user for a Yes/No confirmation."""
    while True:
        try:
            print(f"\n{prompt}")
            print("1 Yes")
            print("2 No")
            choice = input("Select an option (1-2): ").strip()
            
            if choice == "1":
                return True
            elif choice == "2":
                return False
            else:
                print("\n[Error] Invalid option. Please select 1 or 2.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nConfirmation cancelled.")
            return False
