import pytest
from models.person import Student,Teacher,ExamGrade,ControlGrade
def test_student_role(): assert Student('Test','25-12').role()=='Студент'
def test_teacher_role(): assert Teacher('Test').role()=='Оқытушы'
def test_exam_grade(): assert ExamGrade(85).value==85 and ExamGrade(85).grade_type()=='Exam'
def test_control_grade(): assert ControlGrade(65).grade_type()=='Control'
def test_grade_validation():
 with pytest.raises(ValueError): ExamGrade(101)
