# Datheon Python Programming Internship

This repository contains my submissions for the **Datheon Python Programming Internship**. Each task is kept in its own folder with source code and run instructions.

## Table of Contents
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Task 1: Hangman Word Guessing Game](#task-1-hangman-word-guessing-game)
- [Task 2: Stock Portfolio Performance Tracker](#task-2-stock-portfolio-performance-tracker)
- [Skills Demonstrated](#skills-demonstrated)
- [Author](#author)

## Project Structure

```
Datheon_Python_Programming_Internship/
├── README.md
├── Task1_Hangman/
│   ├── hangman.py
│   └── words.txt          (optional custom word list)
└── Task2_Portfolio_Tracker/
    ├── portfolio.py
    ├── sample_prices.csv
    └── portfolio_summary.csv   (generated)
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

## Task 2: Stock Portfolio Performance Tracker

A console utility that tracks an investment portfolio. The user enters ticker symbols, buy prices and share quantities; the program calculates portfolio value and gain/loss, then logs the results to a CSV file.

### Features
- Menu-driven interface: add, view, remove positions, save summary, exit
- Positions stored in a dictionary; re-adding a ticker merges it using weighted-average cost
- Current prices loaded from a CSV file (`sample_prices.csv`); column names (Symbol/Ticker, Price/Close) are detected automatically
- Manual price entry if a ticker is not found in the dataset
- Calculates invested capital, market value, gain/loss and gain/loss % per holding and for the whole portfolio
- Neatly formatted console table with a PROFIT / LOSS status
- Writes `portfolio_summary.csv` (with timestamp and a TOTAL row) using Python's built-in `csv` module
- Input validation and safe file handling

### How to Run
```bash
cd Task2_Portfolio_Tracker
python portfolio.py
```

### Sample Output
```
Ticker     Shares      Buy $      Now $     Invested        Value    Gain/Loss        %
AAPL        15.00     203.33     228.50     3,050.00     3,427.50      +377.50  +12.38%
XYZ          4.00      50.00      88.00       200.00       352.00      +152.00  +76.00%
TOTAL                                       3,250.00     3,779.50      +529.50  +16.29%
Overall portfolio status: PROFIT
```

### Using the S&P 500 Dataset
Download the provided CSV, place it in the `Task2_Portfolio_Tracker` folder, and change `PRICES_FILE` at the top of `portfolio.py` to its file name.

### Concepts Used
Dictionaries, CSV reading/writing, file I/O, functions, loops, input validation, number formatting, error handling.

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
