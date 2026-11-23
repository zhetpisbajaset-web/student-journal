from models.student import Student
from models.grade import ExamGrade, ControlGrade


def test_student_role():
    s = Student("Aset", "IS-21")
    assert s.get_role() == "Student"


def test_student_str():
    s = Student("Aset", "IS-21")
    assert str(s) == "Aset (IS-21)"


def test_exam_grade_weight():
    g = ExamGrade(1, "Math", 80)
    assert g.weighted_score() == 80


def test_control_grade_weight():
    g = ControlGrade(1, "Math", 80)
    assert g.weighted_score() == 40