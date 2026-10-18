# Datheon Python Programming Internship

This repository contains my submissions for the **Datheon Python Programming Internship**. Each task is kept in its own folder with source code and run instructions.

## Table of Contents
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Task 1: Hangman Word Guessing Game](#task-1-hangman-word-guessing-game)
- [Task 2: TASK NAME HERE](#task-2-task-name-here)
- [Skills Demonstrated](#skills-demonstrated)
- [Author](#author)

## Project Structure

```
Datheon_Python_Programming_Internship/
├── README.md
├── Task1_Hangman/
│   ├── hangman.py
│   └── words.txt          (optional custom word list)
└── Task2_TASK_FOLDER/
    └── task2_file.py
```

## Requirements
- Python 3.8 or higher
- No external packages needed (standard library only)
- Any editor: VS Code / PyCharm

---

## Task 1: Hangman Word Guessing Game

A terminal-based Hangman game where the player guesses a hidden word one letter at a time within **6 attempts**.

### Features
- Random word selection using `random.choice()`
- Masked word display (e.g. `_ I _ _ I O N A _ _`)
- ASCII gallows art that updates with every incorrect guess
- Tracks guessed letters using a `set` and shows wrong guesses
- **No penalty for duplicate guesses**: repeating a letter just shows a message
- Input validation: only a single letter (A-Z) is accepted
- Clean victory and defeat screens, with a play-again option
- Loads words from `words.txt` if present, otherwise uses a built-in word list

### How to Run
```bash
cd Task1_Hangman
python hangman.py
```

### Sample Gameplay
```
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========

  Word:   _ I _ _ I O _ A _ _
  Wrong:  E Q U
  Lives:  3/6

Guess a letter:
```

### Code Structure
| Function | Purpose |
|---|---|
| `load_words()` | Reads `words.txt` or falls back to the default list |
| `choose_word()` | Picks a random secret word |
| `mask_word()` | Builds the masked string from guessed letters |
| `display_state()` | Prints gallows art, word, wrong letters and lives |
| `get_guess()` | Validates input and blocks duplicate penalties |
| `play_round()` | Main game loop with win/lose conditions |
| `main()` | Entry point with the replay loop |

### Concepts Used
String manipulation, sets, lists, loops, functions (modular design), file handling, input validation, control flow.

---

## Task 2: TASK NAME HERE

Short description of what the program does.

### Features
- Feature 1
- Feature 2
- Feature 3

### How to Run
```bash
cd Task2_TASK_FOLDER
python task2_file.py
```

---

## Skills Demonstrated
- Writing clean, modular Python code
- Working with strings, sets, and control flow
- Handling user input and edge cases
- Organizing a project with clear folder structure and documentation

## Author
**YOUR NAME**
GitHub: [@your-username](https://github.com/your-username)
LinkedIn: [Your Name](https://www.linkedin.com/in/your-profile)
