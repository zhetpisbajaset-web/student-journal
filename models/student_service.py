from database import get_connection
from models.student import Student


def add_student(student):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, group_name) VALUES (?, ?)",
        (student.name, student.group_name),
    )
    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, group_name FROM students")
    rows = cur.fetchall()
    conn.close()
    return [Student(r[1], r[2], r[0]) for r in rows]


def update_student(student_id, name, group_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name = ?, group_name = ? WHERE id = ?",
        (name, group_name, student_id),
    )
    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()