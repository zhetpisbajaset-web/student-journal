from abc import ABC, abstractmethod
class Person(ABC):
    def __init__(self, full_name):
        self.__full_name = full_name.strip()
        if not self.__full_name: raise ValueError('Аты-жөні бос болмауы керек')
    @property
    def full_name(self): return self.__full_name
    @abstractmethod
    def role(self): pass
class Student(Person):
    def __init__(self, full_name, group_name, student_number=''):
        super().__init__(full_name); self.group_name=group_name; self.student_number=student_number
    def role(self): return 'Студент'
class Teacher(Person):
    def __init__(self, full_name, subject=''):
        super().__init__(full_name); self.subject=subject
    def role(self): return 'Оқытушы'
class Grade(ABC):
    def __init__(self, value):
        self.__value=int(value)
        if not 0 <= self.__value <= 100: raise ValueError('Баға 0–100 аралығында болуы керек')
    @property
    def value(self): return self.__value
    @abstractmethod
    def grade_type(self): pass
class ExamGrade(Grade):
    def grade_type(self): return 'Exam'
class ControlGrade(Grade):
    def grade_type(self): return 'Control'
