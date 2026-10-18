#!/usr/bin/env python3
"""Hangman Word Guessing Game (Console)

A modular terminal game demonstrating string manipulation and control flow.
Run:  python hangman.py
Optional: place a 'words.txt' (one word per line) next to this file to use
a custom English word list; otherwise a built-in list is used.
"""

import os
import random

MAX_MISTAKES = 6

DEFAULT_WORDS = [
    "python", "variable", "function", "iterator", "algorithm", "database",
    "keyboard", "compiler", "terminal", "software", "developer", "network",
    "library", "package", "debugger", "recursion", "boolean", "integer",
    "dictionary", "exception", "inheritance", "interface", "framework",
]

# ASCII gallows stages: index = number of incorrect guesses (0-6)
STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========""",
]


def load_words(path="words.txt"):
    """Load words from a file if present, else fall back to the built-in list."""
    full = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if os.path.exists(full):
        with open(full, encoding="utf-8") as f:
            words = [w.strip().lower() for w in f if w.strip().isalpha() and len(w.strip()) >= 4]
        if words:
            return words
    return DEFAULT_WORDS


def choose_word(words):
    return random.choice(words).lower()


def mask_word(word, guessed):
    """Return masked string, e.g. '_ A _ H E O N'."""
    return " ".join(c.upper() if c in guessed else "_" for c in word)


def display_state(word, guessed, wrong, mistakes):
    print(STAGES[mistakes])
    print(f"\n  Word:   {mask_word(word, guessed)}")
    print(f"  Wrong:  {' '.join(sorted(c.upper() for c in wrong)) or '-'}")
    print(f"  Lives:  {MAX_MISTAKES - mistakes}/{MAX_MISTAKES}\n")


def get_guess(guessed, wrong):
    """Prompt until a valid, not-previously-guessed single letter is entered."""
    while True:
        raw = input("Guess a letter: ").strip().lower()
        if len(raw) != 1 or not raw.isalpha():
            print("  Please enter a single letter (A-Z).")
        elif raw in guessed or raw in wrong:
            print(f"  You already guessed '{raw.upper()}'. No penalty - try another.")
        else:
            return raw


def show_victory(word, mistakes):
    print("\n" + "=" * 36)
    print("   *** VICTORY! YOU SAVED HIM! ***")
    print(f"   The word was: {word.upper()}")
    print(f"   Mistakes made: {mistakes}")
    print("=" * 36)


def show_defeat(word):
    print(STAGES[MAX_MISTAKES])
    print("\n" + "=" * 36)
    print("   xxx GAME OVER - YOU LOST xxx")
    print(f"   The word was: {word.upper()}")
    print("=" * 36)


def play_round(words):
    word = choose_word(words)
    guessed, wrong = set(), set()
    mistakes = 0

    print("\nWelcome to HANGMAN! Guess the word letter by letter.")
    while mistakes < MAX_MISTAKES:
        display_state(word, guessed, wrong, mistakes)
        letter = get_guess(guessed, wrong)

        if letter in word:
            guessed.add(letter)
            print(f"  Good guess! '{letter.upper()}' is in the word.")
            if set(word) <= guessed:
                display_state(word, guessed, wrong, mistakes)
                show_victory(word, mistakes)
                return
        else:
            wrong.add(letter)
            mistakes += 1
            print(f"  Sorry, '{letter.upper()}' is not in the word.")

    show_defeat(word)


def main():
    words = load_words()
    while True:
        play_round(words)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
