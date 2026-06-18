import tkinter as tk
from tkinter import messagebox


def add_task():
    """Adds a task from the entry box to the list text box."""
    task = task_entry.get().strip()
    if task:
        # Check if it's the default placeholder text
        if task != "Type a new task here...":
            # Add bullet point and formatting
            task_list.insert(tk.END, f"  •  {task}\n")
            task_entry.delete(0, tk.END)
            update_placeholder(None)
    else:
        messagebox.showwarning("Warning", "You cannot add an empty task!")


def delete_task():
    """Deletes the currently highlighted text or task."""
    try:
        # Delete selected text in the text widget
        task_list.delete(tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        messagebox.showinfo("Tip", "Highlight the text you want to delete first!")


def clear_all():
    """Clears the entire list."""
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
        task_list.delete("1.0", tk.END)


# --- Placeholder Helpers for a Modern Look ---
def clear_placeholder(event):
    if task_entry.get() == "Type a new task here...":
        task_entry.delete(0, tk.END)
        task_entry.config(fg="#FFFFFF")  # Change text to white when typing


def update_placeholder(event):
    if not task_entry.get().strip():
        task_entry.delete(0, tk.END)
        task_entry.insert(0, "Type a new task here...")
        task_entry.config(fg="#888888")  # Gray placeholder text


# --- GUI Layout Setup ---
root = tk.Tk()
root.title("TaskFlow Studio")
root.geometry("450x550")
root.config(bg="#1E1E24")  # Premium Dark Charcoal Background

# 1. Title Banner
title_label = tk.Label(
    root,
    text="❤️ TaskFlow",
    font=("Helvetica", 24, "bold"),
    bg="#1E1E24",
    fg="#6C5CE7",  # Modern Electric Purple
)
title_label.pack(pady=20)

# 2. Entry Box Frame (Input Area)
input_frame = tk.Frame(root, bg="#1E1E24")
input_frame.pack(pady=10)

task_entry = tk.Entry(
    input_frame,
    font=("Helvetica", 12),
    bg="#2D2D35",
    fg="#888888",
    bd=0,
    border=28,
    insertbackground="white",  # Text cursor color
    width=26,
)
task_entry.insert(0, "Type a new task here...")
# Bind events for placeholder behavior
task_entry.bind("<FocusIn>", clear_placeholder)
task_entry.bind("<FocusOut>", update_placeholder)
task_entry.pack(side=tk.LEFT, padx=5, ipady=8)  # ipady adds internal padding (taller box)

add_button = tk.Button(
    input_frame,
    text="Add Task",
    font=("Helvetica", 10, "bold"),
    bg="#6C5CE7",
    fg="white",
    bd=0,
    activebackground="#5B4BC4",
    activeforeground="white",
    cursor="hand2",
    command=add_task,
)
add_button.pack(side=tk.LEFT, padx=5, ipady=6, ipadx=10)

# 3. Task Display Area (Text Box)
# Using a Text widget instead of a Listbox allows for smoother scrolling and modern text selection
task_list = tk.Text(
    root,
    font=("Helvetica", 13),
    bg="#2D2D35",
    fg="#E0E0E0",
    bd=0,
    padx=15,
    pady=15,
    spacing3=8,  # Adds space between paragraphs/tasks
    width=38,
    height=14,
)
task_list.pack(pady=15)

# 4. Action Buttons Frame (Footer)
button_frame = tk.Frame(root, bg="#1E1E24")
button_frame.pack(pady=10)

delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    font=("Helvetica", 10, "bold"),
    bg="#FF7675",  # Pastel Red
    fg="white",
    bd=0,
    activebackground="#E84393",
    activeforeground="white",
    cursor="hand2",
    command=delete_task,
)
delete_button.pack(side=tk.LEFT, padx=10, ipady=6, ipadx=8)

clear_button = tk.Button(
    button_frame,
    text="Clear All",
    font=("Helvetica", 10, "bold"),
    bg="#74B9FF",  # Pastel Blue
    fg="white",
    bd=0,
    activebackground="#0984E3",
    activeforeground="white",
    cursor="hand2",
    command=clear_all,
)
clear_button.pack(side=tk.LEFT, padx=10, ipady=6, ipadx=8)

root.mainloop()