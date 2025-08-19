import readline
from db import init_db
from utils import clear_screen, pause, print_table
from habits import add_habit, reset_habit, show_history, delete_habit, get_all_habits

HELP_TEXT = """
Available commands:
  add <habit>       → add a new habit
  reset <habit>     → reset streak for habit
  history <habit>   → show streak history
  delete <habit>    → delete a habit completely
  help              → show this help message
  exit              → quit program
"""

COMMANDS = ['add', 'reset', 'history', 'delete', 'help', 'exit']

def completer(text, state):
    """Autocomplete for readline"""
    buffer = readline.get_line_buffer().split()
    habits = [h['name'] for h in get_all_habits()]
    options = []
    if len(buffer) == 0:
        options = [c for c in COMMANDS if c.startswith(text)]
    elif len(buffer) == 1:
        options = [c for c in COMMANDS if c.startswith(buffer[0])]
    else:
        # complete habit names
        options = [h for h in habits if h.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind('tab: complete')
readline.set_completer(completer)

def main():
    init_db()
    try:
        while True:
            clear_screen()
            habits = get_all_habits()
            if habits:
                print_table(habits)
            else:
                print("⚠ No habits yet. Use the 'help' command to learn how to start.")

            cmd = input("\nCommand: ").strip()
            if not cmd:
                continue

            if cmd.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            if cmd.lower() == "help":
                print(HELP_TEXT)
                pause()
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None

            if action == "add" and arg:
                add_habit(arg)
                pause()
            elif action == "reset" and arg:
                reset_habit(arg)
                pause()
            elif action == "history" and arg:
                show_history(arg)
                pause()
            elif action == "delete" and arg:
                delete_habit(arg)
                pause()
            else:
                print("❌ Unknown command. Type 'help' to see available commands.")
                pause()

    except (KeyboardInterrupt, EOFError):
        print("\n👋 Exiting Habit Tracker. Goodbye!")

if __name__ == "__main__":
    main()
