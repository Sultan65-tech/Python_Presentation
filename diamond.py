import tkinter as tk
from tkinter import messagebox
import database as db

# Initialize Database on startup
db.init_db()


def refresh_list():
    """Clears the listbox and reloads active tasks from the DB."""
    task_listbox.delete(0, tk.END)
    global active_tasks_mapping
    # Keep track of database IDs matching the listbox index positions
    active_tasks_mapping = db.get_active_tasks()

    for task in active_tasks_mapping:
        task_listbox.insert(tk.END, task[1])  # task[1] is the task_text


def submit_task():
    """Adds a task from the input field to the DB."""
    text = task_entry.get().strip()
    if text:
        db.add_task(text)
        task_entry.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")


def complete_task():
    """Marks selected task as Completed in DB."""
    try:
        selected_index = task_listbox.curselection()[0]
        task_id = active_tasks_mapping[selected_index][0]

        db.update_task_status(task_id, "Completed")
        refresh_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task first!")


def delete_task():
    """Marks selected task as Deleted in DB instead of dropping it entirely."""
    try:
        selected_index = task_listbox.curselection()[0]
        task_id = active_tasks_mapping[selected_index][0]

        db.update_task_status(task_id, "Deleted")
        refresh_list()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task first!")


def show_progress():
    """Pulls data from the last 7 days and displays it in an alert box."""
    stats = db.get_weekly_progress()
    total = sum(stats.values())

    progress_report = (
        f"--- 7-Day Progress Report ---\n\n"
        f"✅ Completed: {stats['Completed']}\n"
        f"❌ Deleted/Dropped: {stats['Deleted']}\n"
        f"⏳ Still Pending: {stats['Pending']}\n\n"
        f"Total tracked items: {total}"
    )
    messagebox.showinfo("Weekly Stats", progress_report)


# --- GUI Setup ---
root = tk.Tk()
root.title("To-Do List with Progress Tracker")
root.geometry("400x450")
root.config(bg="#f4f4f9")

# Entry and Add Button Frame
input_frame = tk.Frame(root, bg="#f4f4f9")
input_frame.pack(pady=15)

task_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=25)
task_entry.pack(side="left", padx=5)

add_btn = tk.Button(
    input_frame, text="Add Task", bg="#4A90E2", fg="white", command=submit_task
)
add_btn.pack(side="left")

# Listbox for holding active tasks
task_listbox = tk.Listbox(
    root, font=("Helvetica", 11), width=38, height=12, selectbackground="#4A90E2"
)
task_listbox.pack(pady=10)

# Action Buttons Frame
action_frame = tk.Frame(root, bg="#f4f4f9")
action_frame.pack(pady=10)

done_btn = tk.Button(
    action_frame, text="Complete", bg="#2ECC71", fg="white", command=complete_task
)
done_btn.pack(side="left", padx=10)

del_btn = tk.Button(
    action_frame, text="Delete", bg="#E74C3C", fg="white", command=delete_task
)
del_btn.pack(side="left", padx=10)

# Progress Report Button
progress_btn = tk.Button(
    root,
    text="View Weekly Progress Report",
    font=("Helvetica", 10, "bold"),
    bg="#9B59B6",
    fg="white",
    command=show_progress,
)
progress_btn.pack(pady=15, fill="x", padx=40)

# Initial load of items on execution
active_tasks_mapping = []
refresh_list()

root.mainloop()