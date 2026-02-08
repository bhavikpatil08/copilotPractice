"""
Armstrong Number Calculator and Test Cases Module

This module provides functionality to:
- Calculate and identify Armstrong numbers (narcissistic numbers)
- Accept user input for validation
- Generate test cases
- Log errors to a file
- Follow best practices with proper documentation and code organization

An Armstrong number is a number that is equal to the sum of its digits 
each raised to the power of the number of digits.
Example: 153 = 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153
"""

import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    filename='armstrong_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def is_armstrong_number(number: int) -> bool:
    """
    Check if a given number is an Armstrong number.
    
    Args:
        number: Integer to check
        
    Returns:
        bool: True if the number is an Armstrong number, False otherwise
        
    Raises:
        ValueError: If the number is negative
    """
    try:
        if number < 0:
            raise ValueError("Number must be non-negative")
            
        num_str = str(number)
        num_digits = len(num_str)
        sum_of_powers = sum(int(digit) ** num_digits for digit in num_str)
        
        return sum_of_powers == number
        
    except Exception as e:
        logging.error(f"Error in is_armstrong_number for {number}: {str(e)}")
        raise


def get_user_input() -> int:
    """
    Prompt user for a number with input validation.
    
    Returns:
        int: Valid non-negative integer from user
    """
    while True:
        try:
            user_input = input("Enter a number to check if it's an Armstrong number: ")
            number = int(user_input)
            
            if number < 0:
                print("Please enter a non-negative number.")
                continue
                
            return number
            
        except ValueError as e:
            print(f"Invalid input. Please enter a valid integer.")
            logging.error(f"Invalid input from user: {user_input}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            logging.info("User cancelled operation")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            logging.error(f"Unexpected error in get_user_input: {str(e)}")


def generate_test_cases() -> List[Tuple[int, bool]]:
    """
    Generate test cases for Armstrong number validation.
    
    Returns:
        List[Tuple[int, bool]]: List of tuples containing (number, expected_result)
    """
    test_cases = [
        (0, True),      # Single digit
        (1, True),      # Single digit
        (5, True),      # Single digit
        (9, True),      # Single digit
        (10, False),    # Two digits - not Armstrong
        (153, True),    # Three digits - Armstrong
        (370, True),    # Three digits - Armstrong
        (371, True),    # Three digits - Armstrong
        (407, True),    # Three digits - Armstrong
        (100, False),   # Three digits - not Armstrong
        (1634, True),   # Four digits - Armstrong
        (8208, True),   # Four digits - Armstrong
        (9474, True),   # Four digits - Armstrong
        (1000, False),  # Four digits - not Armstrong
        (54748, True),  # Five digits - Armstrong
        (92727, True),  # Five digits - Armstrong
        (93084, True),  # Five digits - Armstrong
    ]
    return test_cases


def run_test_cases() -> None:
    """
    Execute all test cases and display results.
    """
    print("\n" + "="*60)
    print("Running Test Cases for Armstrong Number Checker")
    print("="*60)
    
    test_cases = generate_test_cases()
    passed = 0
    failed = 0
    
    for number, expected in test_cases:
        try:
            result = is_armstrong_number(number)
            status = "PASS" if result == expected else "FAIL"
            
            if result == expected:
                passed += 1
            else:
                failed += 1
                logging.error(f"Test failed for {number}: expected {expected}, got {result}")
            
            print(f"Number: {number:6d} | Expected: {str(expected):5s} | "
                  f"Got: {str(result):5s} | Status: {status}")
                  
        except Exception as e:
            failed += 1
            print(f"Number: {number:6d} | ERROR: {str(e)}")
            logging.error(f"Test case error for {number}: {str(e)}")
    
    print("="*60)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(test_cases)} total")
    print("="*60 + "\n")


def main() -> None:
    """
    Main function to run the Armstrong number calculator.
    """
    try:
        print("\n" + "="*60)
        print("Armstrong Number Calculator")
        print("="*60)
        
        # Run test cases first
        run_test_cases()
        
        # Get user input and check
        while True:
            try:
                number = get_user_input()
                
                if is_armstrong_number(number):
                    print(f"\n✓ {number} is an Armstrong number!")
                else:
                    print(f"\n✗ {number} is NOT an Armstrong number.")
                
                # Ask if user wants to continue
                continue_choice = input("\nDo you want to check another number? (y/n): ").lower()
                if continue_choice != 'y':
                    print("Thank you for using Armstrong Number Calculator!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\nProgram terminated by user.")
                break
                
    except Exception as e:
        print(f"A critical error occurred: {str(e)}")
        logging.error(f"Critical error in main: {str(e)}")


if __name__ == "__main__":
    main()