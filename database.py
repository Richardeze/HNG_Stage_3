import sqlite3
from datetime import datetime, timedelta

DB_NAME = "habits.db"


def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table():
    """Create the habits table if it does not  already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            habit TEXT NOT NULL,
            frequency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_done TIMESTAMP DEFAULT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_habit(username, habit, frequency):
    """Add a new habit to the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if this user already has that habit
    cursor.execute("SELECT * FROM habits WHERE username = ? AND habit = ?", (username, habit))
    existing = cursor.fetchone()

    if existing:
        print(f"'{habit}' already exists for {username}. Skipping insertion.")
    else:
        cursor.execute("INSERT INTO habits (username, habit, frequency) VALUES (?, ?, ?)",
                       (username, habit, frequency))
        conn.commit()
        print(f"Added '{habit}' for {username}")

    conn.close()

def mark_habit_done(username, habit):
    #Mark a habit as done for the current date.
    conn = get_connection()
    cursor = conn.cursor()

    # Update the last_done field
    cursor.execute("""
        UPDATE habits
        SET last_done = CURRENT_TIMESTAMP
        WHERE username = ? AND habit = ?
    """, (username, habit))
    conn.commit()

    if cursor.rowcount > 0:
        message = f"✅ '{habit}' marked as done for {username}."
    else:
        message = f"⚠️ No habit named '{habit}' found for {username}."

    conn.close()
    return message


def is_habit_due(created_at, frequency, last_done=None):
    date_to_check = last_done or created_at
    created_date = datetime.strptime(date_to_check, "%Y-%m-%d %H:%M:%S")
    days_passed = (datetime.now() - created_date).days

    if frequency == "daily" and days_passed >= 1:
        return True
    elif frequency == "weekly" and days_passed >= 7:
        return True
    elif frequency == "biweekly" and days_passed >= 14:
        return True
    elif frequency == "every 2 days" and days_passed >= 2:
        return True
    elif frequency == "monthly" and days_passed >= 30:
        return True
    return False

def get_habits(username):
    """Retrieve all habits for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, habit, frequency, created_at, last_done FROM habits WHERE username = ?", (username,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for habit_id, habit, frequency, created_at, last_done in rows:
        status_icon = ""
        if last_done:
            try:
                last_done_date = datetime.fromisoformat(last_done).date()
                if last_done_date == date.today():
                    status_icon = "✅"
            except ValueError:
                pass  # In case of invalid timestamp format

        if is_habit_due(created_at, frequency, last_done):
            reminder = f"⏰ Reminder: It's time to do your '{habit}' habit ({frequency})."
        else:
            reminder = "✅ You're on track!"
        result.append({
            "id": habit_id,
            "habit": habit,
            "frequency": frequency,
            "created_at": created_at,
            "last_done": last_done,
            "reminder": reminder
        })
    return result

def close_conn():
    conn = get_connection()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Database and table created successfully.")