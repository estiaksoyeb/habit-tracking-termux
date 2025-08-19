import os

def clear_screen():
    os.system("clear")  # Works in Termux/Linux

def pause():
    input("\nPress Enter to continue...")

def print_table(habits):
    col1_width = 15
    col2_width = 30  # wide enough for emoji + text
    print(f"\n{'Habit Name':<{col1_width}} | {'Current Streak':<{col2_width}}")
    print("-" * (col1_width + col2_width + 3))
    for h in habits:
        print(f"{h['name']:<{col1_width}} | {h['streak']:<{col2_width}}")
