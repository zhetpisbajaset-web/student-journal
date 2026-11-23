from abc import ABC, abstractmethod


class Grade(ABC):
    def __init__(self, student_id, subject, score):
        self._student_id = student_id
        self._subject = subject
        self._score = score

    @property
    def student_id(self):
        return self._student_id

    @property
    def subject(self):
        return self._subject

    @property
    def score(self):
        return self._score

    @abstractmethod
    def get_weight(self):
        pass

    def weighted_score(self):
        return self._score * self.get_weight()


class ExamGrade(Grade):
    def get_weight(self):
        return 1.0


class ControlGrade(Grade):
    def get_weight(self):
        return 0.5