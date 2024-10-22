import random
import tkinter as tk
from tkinter import ttk

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")

        self.playing = False
        self.word_to_guess = ""
        self.displayed_word = ""
        self.remaining_attempts = 5
        self.guessed_letters = []

        self.word_hints = {
            'january': 'The first month of the year',
            'border': 'A line separating two political or geographical areas',
            'image': 'A representation of the external form of a person or thing',
            'film': 'A motion picture',
            'promise': 'A declaration or assurance that one will do a particular thing',
            'kids': 'Children',
            'lungs': 'Respiratory organs',
            'doll': 'A child\'s toy',
            'rhyme': 'Correspondence of sound between words',
            'damage': 'Physical harm that impairs the value or usefulness of something',
            'plants': 'Living organisms that typically have roots, stems, and leaves',
            'hello': 'A common greeting',
            'world': 'The earth, together with all of its countries and peoples'
        }

        self.initialize_ui()

    def initialize_ui(self):
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Century Gothic", 16), background="white")
        self.style.configure("TButton", font=("Century Gothic", 14), background="white")
        self.style.configure("TEntry", font=("Century Gothic", 14), background="white")

        self.background_image = tk.PhotoImage(file="hangmanbg.gif")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.word_label = ttk.Label(self.root, text="", style="TLabel")
        self.hint_label = ttk.Label(self.root, text="", style="TLabel", foreground="gray")
        self.attempts_label = ttk.Label(self.root, text="", style="TLabel")
        self.entry = ttk.Entry(self.root, font=("Arial", 14), style="TEntry")
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.check_guess, style="TButton")
        self.restart_button = ttk.Button(self.root, text="Restart", command=self.restart_game, style="TButton")
        self.message_label = ttk.Label(self.root, text="", style="TLabel")

        self.word_label.pack(pady=50)
        self.hint_label.pack()
        self.attempts_label.pack()
        self.entry.pack(pady=10)
        self.submit_button.pack()
        self.restart_button.pack()
        self.message_label.pack()

        self.play_hangman()

    def display_message(self, message, timeout=2000, color="black"):
        self.message_label.config(text=message, foreground=color)
        self.root.after(timeout, self.clear_message)

    def clear_message(self):
        self.message_label.config(text="")

    def play_hangman(self):
        self.playing = True
        self.word_to_guess = random.choice(list(self.word_hints.keys()))
        self.displayed_word = '_' * len(self.word_to_guess)
        self.remaining_attempts = 5
        self.guessed_letters = []

        self.word_label.config(text=self.displayed_word)
        self.hint_label.config(text=f"Hint: {self.word_hints[self.word_to_guess]}")
        self.attempts_label.config(text=f"Attempts remaining: {self.remaining_attempts}")
        self.restart_button.config(state=tk.DISABLED)

    def check_guess(self):
        if not self.playing:
            return

        guess = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.display_message("Invalid input. Please enter a single letter.", color="red")
            return

        if guess in self.guessed_letters:
            self.display_message(f"You already guessed '{guess}'. Try again.", color="red")
            return

        if guess in self.word_to_guess:
            self.guessed_letters.append(guess)
            for i, letter in enumerate(self.word_to_guess):
                if letter == guess:
                    self.displayed_word = self.displayed_word[:i] + guess + self.displayed_word[i + 1:]
            self.word_label.config(text=self.displayed_word)

            if self.displayed_word == self.word_to_guess:
                self.display_message(f"Congrats! You have guessed the word '{self.word_to_guess}' correctly!",
                                     color="green")
                self.restart_button.config(state=tk.NORMAL)
                self.playing = False
                return
        else:
            self.guessed_letters.append(guess)
            self.remaining_attempts -= 1
            self.attempts_label.config(text=f"Attempts remaining: {self.remaining_attempts}")

            if self.remaining_attempts == 0:
                self.display_message(f"Wrong guess. You've been hanged! The word was: {self.word_to_guess}",
                                     color="red")
                self.restart_button.config(state=tk.NORMAL)
                self.playing = False
                return

    def restart_game(self):
        self.play_hangman()
        self.restart_button.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
