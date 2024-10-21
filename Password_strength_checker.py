# password strength checker :


import string
import getpass
import re


def calculate_entropy(password):
    """Calculates entropy for better password strength measurement."""
    pool_size = 0
    if re.search(r'[a-z]', password):  # lowercase
        pool_size += 26
    if re.search(r'[A-Z]', password):  # uppercase
        pool_size += 26
    if re.search(r'[0-9]', password):  # digits
        pool_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # special characters
        pool_size += len(string.punctuation)

    # Entropy calculation formula
    entropy = len(password) * (pool_size.bit_length() - 1)
    return entropy


def check_password_strength():
    password = getpass.getpass('Enter the password: ')
    lower_count = len(re.findall(r'[a-z]', password))
    upper_count = len(re.findall(r'[A-Z]', password))
    num_count = len(re.findall(r'[0-9]', password))
    special_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
    length = len(password)

    strength = 0

    if length >= 8:
        strength += 1
    if lower_count >= 1:
        strength += 1
    if upper_count >= 1:
        strength += 1
    if num_count >= 1:
        strength += 1
    if special_count >= 1:
        strength += 1

    entropy = calculate_entropy(password)

    # Password feedback based on strength
    if strength <= 2:
        remarks = ('That\'s a weak password. You should add more variety of characters, '
                   'including uppercase, lowercase, digits, and special symbols.')
    elif strength == 3:
        remarks = 'Your password is okay, but it could be stronger.'
    elif strength == 4:
        remarks = 'Your password is strong, but consider adding more length or variety.'
    else:
        remarks = ('Now that\'s one hell of a strong password!!! Hackers don\'t stand a chance!')

    print('Your password has:')
    print(f'{lower_count} lowercase letters')
    print(f'{upper_count} uppercase letters')
    print(f'{num_count} digits')
    print(f'{special_count} special characters')
    print(f'Password Length: {length}')
    print(f'Password Entropy: {entropy:.2f} bits')
    print(f'Strength Score: {strength}/5')
    print(f'Remarks: {remarks}')


def check_pwd(another_pw=False):
    while True:
        if another_pw:
            choice = input('Do you want to check another password\'s strength (y/n): ')
        else:
            choice = input('Do you want to check your password\'s strength (y/n): ')

        if choice.lower() == 'y':
            return True
        elif choice.lower() == 'n':
            print('Exiting...')
            return False
        else:
            print('Invalid input...please try again.')


if __name__ == '__main__':
    print('===== Welcome to Password Strength Checker =====')
    check_pw = check_pwd()
    while check_pw:
        check_password_strength()
        check_pw = check_pwd(True)
