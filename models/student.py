from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name):
        self._name = name  # инкапсуляция

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_role(self):
        pass


class Student(Person):
    def __init__(self, name, group_name, student_id=None):
        super().__init__(name)
        self._group_name = group_name
        self._id = student_id

    @property
    def group_name(self):
        return self._group_name

    @property
    def id(self):
        return self._id

    def get_role(self):
        return "Student"

    def __str__(self):
        return f"{self._name} ({self._group_name})"