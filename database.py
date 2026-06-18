from datetime import datetime, timedelta
import sqlite3


def init_db():
    """Initializes the database and creates the tasks table."""
    conn = sqlite3.connect("todo_progress.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            status TEXT NOT NULL, -- 'Pending', 'Completed', 'Deleted'
            updated_at TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def add_task(text):
    """Inserts a new pending task."""
    conn = sqlite3.connect("todo_progress.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO tasks (task_text, status, updated_at) VALUES (?, 'Pending', ?)",
        (text, now),
    )
    conn.commit()
    conn.close()


def update_task_status(task_id, new_status):
    """Changes status to 'Completed' or 'Deleted' and updates the timestamp."""
    conn = sqlite3.connect("todo_progress.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
        (new_status, now, task_id),
    )
    conn.commit()
    conn.close()


def get_active_tasks():
    """Fetches all tasks that are currently 'Pending'."""
    conn = sqlite3.connect("todo_progress.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_text FROM tasks WHERE status = 'Pending'")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def get_weekly_progress():
    """Fetches stats for tasks updated within the last 7 days."""
    conn = sqlite3.connect("todo_progress.db")
    cursor = conn.cursor()

    # Calculate date from 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        SELECT status, COUNT(*) 
        FROM tasks 
        WHERE updated_at >= ? 
        GROUP BY status
    """,
        (seven_days_ago,),
    )

    stats = dict(cursor.fetchall())
    conn.close()

    # Ensure all statuses exist in the dictionary output
    return {
        "Pending": stats.get("Pending", 0),
        "Completed": stats.get("Completed", 0),
        "Deleted": stats.get("Deleted", 0),
    }