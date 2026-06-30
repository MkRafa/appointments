import re
from datetime import datetime, timedelta
from typing import Tuple, Optional
from colorama import Fore, Style, init

init(autoreset=True)

def print_header(text: str) -> None:
    """Print formatted header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}{Style.RESET_ALL}\n")

def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

def print_section(text: str) -> None:
    """Print section header"""
    print(f"\n{Fore.MAGENTA}{text}:{Style.RESET_ALL}")

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    phone = phone.replace(' ', '').replace('-', '')
    return len(phone) >= 10 and phone.replace('+', '').isdigit()

def validate_date(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_str: str) -> bool:
    """Validate time format (HH:MM)"""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_age(date_of_birth: str) -> bool:
    """Validate that patient is at least 1 year old"""
    try:
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
        age = datetime.now().year - dob.year
        return age >= 0 and age <= 150
    except ValueError:
        return False

def get_valid_input(prompt: str, validation_func=None) -> str:
    """Get valid input from user"""
    while True:
        user_input = input(f"{Fore.CYAN}{prompt}:{Style.RESET_ALL} ").strip()
        if not user_input:
            print_error("Input cannot be empty!")
            continue
        if validation_func and not validation_func(user_input):
            print_error(f"Invalid input format!")
            continue
        return user_input

def get_integer_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Get valid integer input from user"""
    while True:
        try:
            user_input = input(f"{Fore.CYAN}{prompt}:{Style.RESET_ALL} ").strip()
            value = int(user_input)
            if min_val is not None and value < min_val:
                print_error(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print_error(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid number")

def display_list(items: list, show_index: bool = True) -> None:
    """Display list of items with formatting"""
    for idx, item in enumerate(items, 1):
        if show_index:
            print(f"  {Fore.YELLOW}{idx}.{Style.RESET_ALL} {item}")
        else:
            print(f"  • {item}")

def get_date_range(days_ahead: int = 30) -> Tuple[str, str]:
    """Get date range for appointments"""
    today = datetime.now()
    start_date = today + timedelta(days=1)  # Tomorrow
    end_date = today + timedelta(days=days_ahead)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def is_business_hours(time_str: str, opening_time: str, closing_time: str) -> bool:
    """Check if time is within business hours"""
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    opening = datetime.strptime(opening_time, '%H:%M').time()
    closing = datetime.strptime(closing_time, '%H:%M').time()
    return opening <= time_obj <= closing

def calculate_age(date_of_birth: str) -> int:
    """Calculate age from date of birth"""
    dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
    today = datetime.now()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def format_date(date_str: str) -> str:
    """Format date string to readable format"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%A, %B %d, %Y')

def clear_screen() -> None:
    """Clear console screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
