import random
import tkinter as tk
from tkinter import messagebox

def print_welcome():
    messagebox.showinfo("Welcome", """
    ***************************************
             WELCOME TO TREASURE HUNT
    ***************************************
    You are an adventurer seeking treasure.
    Beware of traps and monsters along the way!!
    Reach the treasure to win the game.
    ***************************************
    """)

def choose_path():
    def set_choice(choice):
        nonlocal user_choice
        user_choice = choice
        root.quit()

    user_choice = None
    root = tk.Tk()
    root.title("Choose a Path")
    label = tk.Label(root, text="You are at a crossroad. Choose a path:")
    label.pack()

    tk.Button(root, text="1. Go through the dark forest.", command=lambda: set_choice(1)).pack()
    tk.Button(root, text="2. Cross the haunted bridge.", command=lambda: set_choice(2)).pack()
    tk.Button(root, text="3. Enter the mysterious cave.", command=lambda: set_choice(3)).pack()

    root.mainloop()
    root.destroy()
    return user_choice

def encounter():
    events = ["You find a helpful guide who gives you a map!",
              "A trap activates, and you lose some health!",
              "You meet a monster and must fight!",
              "You find a hidden stash of gold coins!",
              "A riddle-asking troll blocks your way."]
    return random.choice(events)

def handle_encounter(event, health):
    if "trap" in event:
        messagebox.showwarning("Trap!", "Oh no! You lose 10 health points.")
        return health - 10
    elif "monster" in event:
        messagebox.showwarning("Monster!", "You fight bravely and defeat the monster! You lose 20 health points but survive.")
        return health - 20
    elif "gold" in event:
        messagebox.showinfo("Treasure!", "Hurray! You gain 50 gold coins.")
        return health
    elif "guide" in event:
        messagebox.showinfo("Guide!", "The guide's map helps you avoid dangers. No health lost.")
        return health
    elif "riddle" in event:
        answer = simpledialog.askstring("Riddle", "Solve the riddle: What has keys but can't open locks?").lower()
        if answer == "piano":
            messagebox.showinfo("Riddle", "Correct! The troll lets you pass.")
            return health
        else:
            messagebox.showwarning("Riddle", "Wrong! The troll gets angry and takes 10 health points.")
            return health - 10

def treasure_room():
    messagebox.showinfo("Victory", "Congratulations! You've reached the treasure room. A chest of gold and jewels is before you. YOU WIN!")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    print_welcome()
    health = 100
    while health > 0:
        path = choose_path()
        if path is None:
            messagebox.showerror("Error", "You must choose a valid path to continue.")
            continue

        event = encounter()
        messagebox.showinfo("Event", event)
        health = handle_encounter(event, health)

        if health <= 0:
            messagebox.showerror("Game Over", "You have lost all your health. Game Over.")
            break

        if random.randint(1, 5) == 5:  # Random chance to reach treasure
            treasure_room()
            break

if __name__ == "__main__":
    main()
