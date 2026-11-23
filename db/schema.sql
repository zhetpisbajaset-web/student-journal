PRAGMA foreign_keys=ON;
CREATE TABLE groups(id INTEGER PRIMARY KEY, group_name TEXT UNIQUE NOT NULL);
CREATE TABLE students(id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, group_id INTEGER NOT NULL, student_number TEXT UNIQUE, FOREIGN KEY(group_id) REFERENCES groups(id));
CREATE TABLE subjects(id INTEGER PRIMARY KEY, subject_name TEXT UNIQUE NOT NULL, teacher_name TEXT);
CREATE TABLE grades(id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, subject_id INTEGER NOT NULL, grade_value INTEGER CHECK(grade_value BETWEEN 0 AND 100), grade_type TEXT CHECK(grade_type IN ('Exam','Control')), grade_date TEXT NOT NULL, FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY(subject_id) REFERENCES subjects(id));
CREATE TABLE attendance(id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, subject_id INTEGER NOT NULL, lesson_date TEXT NOT NULL, status TEXT CHECK(status IN ('Present','Absent','Late')), FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY(subject_id) REFERENCES subjects(id));
