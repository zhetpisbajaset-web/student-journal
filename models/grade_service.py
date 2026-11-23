from database import get_connection


def add_grade(student_id, subject, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO grades (student_id, subject, score) VALUES (?, ?, ?)",
        (student_id, subject, score),
    )
    conn.commit()
    conn.close()


def mark_attendance(student_id, date, present):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance (student_id, date, present) VALUES (?, ?, ?)",
        (student_id, date, 1 if present else 0),
    )
    conn.commit()
    conn.close()


def get_average(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT AVG(score) FROM grades WHERE student_id = ?", (student_id,))
    result = cur.fetchone()[0]
    conn.close()
    return result if result is not None else 0