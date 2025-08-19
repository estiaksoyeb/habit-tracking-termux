from datetime import datetime
from db import get_conn

def format_timedelta(diff):
    if diff.days > 0:
        hours = diff.seconds // 3600
        return f"{diff.days} days, {hours} hours"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"{hours} hours, {minutes} minutes"
    else:
        minutes = diff.seconds // 60
        seconds = diff.seconds % 60
        return f"{minutes} minutes, {seconds} seconds"

def add_habit(name):
    conn = get_conn()
    cur = conn.cursor()
    try:
        now = datetime.now().isoformat()
        cur.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (name, now))
        hid = cur.lastrowid
        cur.execute("INSERT OR REPLACE INTO current_streak (habit_id, start_datetime) VALUES (?, ?)", (hid, now))
        conn.commit()
        print(f"✅ Added habit '{name}'")
    except:
        print("❌ Habit already exists.")
    conn.close()

def reset_habit(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM habits WHERE name=?", (name,))
    row = cur.fetchone()
    if not row:
        print("❌ Habit not found.")
        conn.close()
        return
    hid = row[0]

    cur.execute("SELECT start_datetime FROM current_streak WHERE habit_id=?", (hid,))
    row = cur.fetchone()
    if row:
        start_dt = datetime.fromisoformat(row[0])
        diff = datetime.now() - start_dt
        streak_text = format_timedelta(diff)

        # Ask optional reason
        reason = input("Optional: Enter reason for reset (press Enter to skip): ").strip()
        if reason == "":
            reason = None

        cur.execute(
            "INSERT INTO streak_history (habit_id, streak_length, fail_date, reason) VALUES (?, ?, ?, ?)",
            (hid, streak_text, datetime.now().isoformat(), reason)
        )
        cur.execute(
            "UPDATE current_streak SET start_datetime=? WHERE habit_id=?",
            (datetime.now().isoformat(), hid)
        )
        conn.commit()
        print(f"💔 Habit '{name}' reset after {streak_text}.")
        if reason:
            print(f"📝 Reason: {reason}")
    conn.close()

def show_history(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM habits WHERE name=?", (name,))
    row = cur.fetchone()
    if not row:
        print("❌ Habit not found.")
        conn.close()
        return
    hid = row[0]

    cur.execute(
        "SELECT streak_length, fail_date, reason FROM streak_history WHERE habit_id=? ORDER BY fail_date",
        (hid,)
    )
    rows = cur.fetchall()
    if not rows:
        print("⚠ No history yet.")
    else:
        print(f"\n📜 History for '{name}':")
        for r in rows:
            line = f"Streak {r[0]} → failed on {r[1]}"
            if r[2]:
                line += f" | Reason: {r[2]}"
            print(line)
    conn.close()

def delete_habit(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM habits WHERE name=?", (name,))
    row = cur.fetchone()
    if not row:
        print("❌ Habit not found.")
        conn.close()
        return
    hid = row[0]
    cur.execute("DELETE FROM habits WHERE id=?", (hid,))
    cur.execute("DELETE FROM current_streak WHERE habit_id=?", (hid,))
    cur.execute("DELETE FROM streak_history WHERE habit_id=?", (hid,))
    conn.commit()
    conn.close()
    print(f"🗑 Habit '{name}' deleted successfully.")

def get_all_habits():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT h.id, h.name, cs.start_datetime FROM habits h LEFT JOIN current_streak cs ON h.id=cs.habit_id"
    )
    rows = cur.fetchall()
    habits = []
    for r in rows:
        streak = "0 seconds"
        if r[2]:
            start_dt = datetime.fromisoformat(r[2])
            diff = datetime.now() - start_dt
            streak = format_timedelta(diff)
        streak = f"🔥 {streak}"
        habits.append({'name': r[1], 'streak': streak})
    conn.close()
    return habits
