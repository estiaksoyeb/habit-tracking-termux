# Habit Tracker for Termux

A lightweight habit tracker for Termux using Python and SQLite.  
Track your habits, streaks, history, and optional reset reasons, all from the command line.

---

## Features

- Add new habits and track them
- Reset habits with optional reason
- View habit streak history
- Shows current streaks with time (minutes, hours, days)
- Delete habits
- Tab-completion for commands and habit names
- Works entirely in Termux

---

## Manual Installation

1. **Download the repository**  

   You can either `git clone` or download the ZIP from GitHub:  

   ```bash
   git clone https://github.com/estiaksoyeb/habit-tracker-termux.git
   cd habit-tracker-termux
    ```

    Or download ZIP and extract it to a folder.

2. **Run the installer**

    ```bash
    bash install.sh
    ```

    This will:
    
    Check for Python and SQLite, install if missing

    Copy all files to ~/.programs/habits/

    Create a habit launcher in Termux $PREFIX/bin/

    Make the launcher executable



3. Run Habit Tracker

    After installation, simply run:

    ```bash
    habit
    ```

    This will launch the habit tracker interface.




---

## Usage

Once launched, you can use commands like:

    add <habit>       # Add a new habit
    reset <habit>     # Reset a habit with optional reason
    history <habit>   # View habit streak history
    delete <habit>    # Delete a habit
    exit              # Exit the program
    help              # Show available commands

### Example

    Command: add nofap
    Command: reset nofap
    Optional: Enter reason for reset (press Enter to skip): porn
    Command: history nofap
---

## License

This repository is licensed under the terms of the MIT License.

---
