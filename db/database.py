import sqlite3
from pathlib import Path
DB=Path(__file__).resolve().parent.parent/'journal.db'
SCHEMA='''PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY, group_name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, group_id INTEGER NOT NULL, student_number TEXT UNIQUE, FOREIGN KEY(group_id) REFERENCES groups(id));
CREATE TABLE IF NOT EXISTS subjects(id INTEGER PRIMARY KEY, subject_name TEXT UNIQUE NOT NULL, teacher_name TEXT);
CREATE TABLE IF NOT EXISTS grades(id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, subject_id INTEGER NOT NULL, grade_value INTEGER CHECK(grade_value BETWEEN 0 AND 100), grade_type TEXT CHECK(grade_type IN ('Exam','Control')), grade_date TEXT NOT NULL, FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY(subject_id) REFERENCES subjects(id));
CREATE TABLE IF NOT EXISTS attendance(id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, subject_id INTEGER NOT NULL, lesson_date TEXT NOT NULL, status TEXT CHECK(status IN ('Present','Absent','Late')), FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY(subject_id) REFERENCES subjects(id));'''
def connect():
 c=sqlite3.connect(DB); c.execute('PRAGMA foreign_keys=ON'); return c
def init_db():
 with connect() as c:
  c.executescript(SCHEMA)
  if c.execute('select count(*) from groups').fetchone()[0]==0: c.executemany('insert into groups(group_name) values(?)',[('25-12',),('25-13',)])
  if c.execute('select count(*) from subjects').fetchone()[0]==0: c.executemany('insert into subjects(subject_name,teacher_name) values(?,?)',[('Бағдарламалау технологиясы','Оқытушы 1'),('Алгоритмдер','Оқытушы 2'),('Операциялық жүйелер','Оқытушы 3')])
  if c.execute('select count(*) from students').fetchone()[0]==0:
   gid=c.execute("select id from groups where group_name='25-12'").fetchone()[0]
   c.executemany('insert into students(full_name,group_id,student_number) values(?,?,?)',[(f'Студент {i}',gid,f'S{i:03}') for i in range(1,11)])
  if c.execute('select count(*) from grades').fetchone()[0]==0:
   st=c.execute('select id from students').fetchall(); su=c.execute('select id from subjects').fetchall()
   c.executemany('insert into grades(student_id,subject_id,grade_value,grade_type,grade_date) values(?,?,?,?,?)',[(sid,su[i%len(su)][0],70+i,'Exam' if i%2==0 else 'Control','2026-11-21') for i,(sid,) in enumerate(st)])
  if c.execute('select count(*) from attendance').fetchone()[0]==0:
   sidlist=c.execute('select id from students').fetchall(); sub=c.execute('select id from subjects limit 1').fetchone()[0]
   c.executemany('insert into attendance(student_id,subject_id,lesson_date,status) values(?,?,?,?)',[(sid,sub,'2026-11-21','Present' if i%3 else 'Absent') for i,(sid,) in enumerate(sidlist)])
if __name__=='__main__': init_db(); print('Дерекқор дайын:',DB)
