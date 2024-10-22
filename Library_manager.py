'''
Library Manager
-------------------------------------------------------------
'''

import json
import sys
from datetime import datetime

class Library:

    def __init__(self, books):
        self.books = books

    def show_avail_books(self):
        print('Our Library Can Offer You The Following Books:')
        print('================================================')
        for book, borrower in self.books.items():
            if borrower == 'Free':
                print(book)

    def lend_book(self, requested_book, name):
        if requested_book in self.books:
            if self.books[requested_book] == 'Free':
                print(
                    f'{requested_book} has been marked'
                    f' as \'Borrowed\' by: {name}')
                self.books[requested_book] = name
                return True
            else:
                print(
                    f'Sorry, the {requested_book} is currently'
                    f' on loan to: {self.books[requested_book]}')
                return False
        else:
            print('The requested book is not available in the library.')
            return False

    def return_book(self, returned_book):
        self.books[returned_book] = 'Free'
        print(f'Thanks for returning {returned_book}')

    def search_books(self, keyword):
        print(f'Search results for "{keyword}":')
        print('================================================')
        found = False
        for book in self.books.keys():
            if keyword.lower() in book.lower():
                found = True
                print(book)
        if not found:
            print(f'No books found with keyword: {keyword}')

    def save_state(self):
        with open('library_books.json', 'w') as f:
            json.dump(self.books, f)
        print('Library state has been saved.')

    def load_state(self):
        try:
            with open('library_books.json', 'r') as f:
                self.books = json.load(f)
            print('Library state has been loaded.')
        except FileNotFoundError:
            print('No previous library state found, using default books.')
            self.books = {
                'The Last Battle': 'Free',
                'The Hunger Games': 'Free',
                'Cracking the Coding Interview': 'Free'
            }


class Student:
    def __init__(self, name, library):
        self.name = name
        self.books = []
        self.library = library

    def view_borrowed(self):
        if not self.books:
            print('You haven\'t borrowed any books.')
        else:
            print(f'Books borrowed by {self.name}:')
            for book, date in self.books:
                print(f'{book} (Borrowed on {date})')

    def request_book(self):
        book = input(
            'Enter the name of the book you\'d like to borrow >> ')
        if len(self.books) >= 3:
            print('You have reached your borrowing limit (3 books). Return a book before borrowing more.')
        elif self.library.lend_book(book, self.name):
            self.books.append((book, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def return_book(self):
        book = input(
            'Enter the name of the book you\'d like to return >> ')
        for borrowed_book, _ in self.books:
            if borrowed_book == book:
                self.library.return_book(book)
                self.books.remove((borrowed_book, _))
                return
        print('You haven\'t borrowed that book, try another...')


def display_menu():
    """ Displays the library menu."""
    print('''
        ==========LIBRARY MENU===========
        1. Display Available Books
        2. Borrow a Book
        3. Return a Book
        4. View Your Books
        5. Search for a Book
        6. Exit
    ''')

def get_user_choice():
    """ Gets user input and ensures it's valid."""
    while True:
        choice = input('Enter Choice (or press q to quit): ').lower()
        if choice in {'1', '2', '3', '4', '5', '6', 'q'}:
            return choice
        else:
            print('Invalid choice, please try again.')

def handle_exit(library):
    """ Handles the process of exiting the system."""
    print('Saving state and exiting...')
    library.save_state()
    sys.exit()

def create_lib():
    library = Library({})
    library.load_state()

    student_name = input("Enter your name: ")
    student = Student(student_name, library)

    # Dictionary to map user choices to corresponding functions
    menu_actions = {
        '1': library.show_avail_books,
        '2': student.request_book,
        '3': student.return_book,
        '4': student.view_borrowed,
        '5': lambda: library.search_books(input('Enter the keyword to search for a book >> ')),
        '6': lambda: handle_exit(library),
        'q': lambda: handle_exit(library)
    }

    # Main loop for user interactions
    while True:
        display_menu()
        choice = get_user_choice()

        # Call the corresponding function from the menu_actions dictionary
        action = menu_actions.get(choice)
        if action:
            action()  # Perform the action corresponding to the user's choice


if __name__ == '__main__':
    create_lib()
