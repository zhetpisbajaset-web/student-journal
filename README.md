# Электрондық студенттер журналы
Python + Tkinter + SQLite оқу жобасы.

## Іске қосу
VS Code-та папканы ашып, терминалда `python -m ui.app` орындаңыз.
Алғаш іске қосқанда journal.db жасалып, 10 үлгі студент, пәндер, бағалар және қатысу деректері енгізіледі.

## Тест
`python -m pip install pytest` және `python -m pytest -v`.

## Құрылым
models/person.py — абстрактілі Person, Student, Teacher және Grade мұрагерлері.
db/database.py, db/schema.sql — SQLite дерекқоры.
ui/app.py — интерфейс.
tests/test_models.py — unit тесттер.
