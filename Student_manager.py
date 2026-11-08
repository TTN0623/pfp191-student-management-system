# Student_manager.py
from Student import Student
from Student_file_helper import StudentFileHelper


class StudentManagerException(Exception):
    """Raised when a student action breaks a business rule."""
    pass
#End class


class StudentManager:
    """
    Holds every student in memory and runs the business rules on them.
    The data lives in a dictionary so that looking a student up by ID is fast.
    """

    def __init__(self):
        self._file_helper = StudentFileHelper()
        # Key: student ID, value: the Student object
        self._student_dict = {}
    #End def

    @property
    def student_dict(self) -> dict:
        """Getter for the whole dictionary. Read-only: there is no setter."""
        return self._student_dict
    #End def

    def load_data(self) -> int:
        """Reads the data file and fills the dictionary. Returns how many students were read."""
        student_list = self._file_helper.load()
        self._student_dict = {}
        for student in student_list:
            self._student_dict[student.student_id] = student
        #End for
        return len(self._student_dict)
    #End def

    def save_data(self) -> None:
        """Writes the whole dictionary back to the data file."""
        self._file_helper.save(list(self._student_dict.values()))
    #End def

    def add_student(self, student: Student) -> None:
        """Adds one student. The ID must not be used yet."""
        if student.student_id in self._student_dict:
            raise StudentManagerException("Student ID " + student.student_id + " already exists.")
        #End if
        self._student_dict[student.student_id] = student
    #End def

    def find_student_by_id(self, student_id: str) -> Student:
        """Returns the student with that ID, or None when nobody has it."""
        return self._student_dict.get(student_id.strip().upper())
    #End def

    def update_student(self, student_id: str, field_name: str, new_value: str) -> None:
        """
        Changes one field of one student. The ID itself cannot be changed
        because it is the key of the dictionary.
        """
        student = self.find_student_by_id(student_id)
        if student is None:
            raise StudentManagerException("No student has the ID " + student_id + ".")
        #End if

        if field_name == "full_name":
            student.full_name = new_value
        elif field_name == "date_of_birth":
            student.date_of_birth = new_value
        elif field_name == "gender":
            student.gender = new_value
        elif field_name == "class_name":
            student.class_name = new_value
        elif field_name == "phone":
            student.phone = new_value
        elif field_name == "email":
            student.email = new_value
        elif field_name == "status":
            student.status = new_value
        else:
            raise StudentManagerException("The field " + field_name + " cannot be changed.")
        #End if
    #End def

    def delete_student(self, student_id: str) -> Student:
        """Removes one student and returns the removed object."""
        student = self.find_student_by_id(student_id)
        if student is None:
            raise StudentManagerException("No student has the ID " + student_id + ".")
        #End if
        del self._student_dict[student.student_id]
        return student
    #End def

    def get_all_student_list(self) -> list:
        """Returns every student as a list."""
        return list(self._student_dict.values())
    #End def

    def search_by_name(self, keyword: str) -> list:
        """Returns every student whose name holds the keyword, ignoring upper or lower case."""
        keyword = keyword.strip().lower()
        student_list = []
        for student in self._student_dict.values():
            if keyword in student.full_name.lower():
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    def search_by_class(self, class_name: str) -> list:
        """Returns every student of one class."""
        class_name = class_name.strip().upper()
        student_list = []
        for student in self._student_dict.values():
            if student.class_name == class_name:
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    def search_by_status(self, status: str) -> list:
        """Returns every student of one study status. Menu item 1.3."""
        status = status.strip().capitalize()
        student_list = []
        for student in self._student_dict.values():
            if student.status == status:
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    def get_active_student_list(self) -> list:
        """Returns every student who is still studying. Menu item 1.4."""
        student_list = []
        for student in self._student_dict.values():
            if student.is_active():
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    def get_sorted_by_name(self) -> list:
        """Returns every student sorted by full name from A to Z."""
        return sorted(self._student_dict.values(), key=lambda student: student.full_name.lower())
    #End def

    def get_sorted_by_id(self) -> list:
        """Returns every student sorted by student ID."""
        return sorted(self._student_dict.values(), key=lambda student: student.student_id)
    #End def

    def count_by_status(self) -> dict:
        """Counts how many students stand in each study status."""
        count_dict = {}
        for status in Student.STATUS_TUPLE:
            count_dict[status] = 0
        #End for
        for student in self._student_dict.values():
            count_dict[student.status] = count_dict.get(student.status, 0) + 1
        #End for
        return count_dict
    #End def

    def get_class_name_set(self) -> set:
        """Returns the set of every class that appears in the data."""
        class_name_set = set()
        for student in self._student_dict.values():
            class_name_set.add(student.class_name)
        #End for
        return class_name_set
    #End def
#End class
