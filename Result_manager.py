# Result_manager.py
from Result import Result
from Result_file_helper import ResultFileHelper


class ResultManagerException(Exception):
    """Raised when a result action breaks a business rule."""
    pass
#End class


class ResultManager:
    """
    Holds every study result in memory and runs the business rules on them.
    The data lives in a list because one student owns many results.
    """

    def __init__(self):
        self._file_helper = ResultFileHelper()
        self._result_list = []
    #End def

    @property
    def result_list(self) -> list:
        """Getter for the whole list. Read-only: there is no setter."""
        return self._result_list
    #End def

    def load_data(self) -> int:
        """Reads the data file into the list. Returns how many results were read."""
        self._result_list = self._file_helper.load()
        return len(self._result_list)
    #End def

    def save_data(self) -> None:
        """Writes the whole list back to the data file."""
        self._file_helper.save(self._result_list)
    #End def

    def add_result(self, result: Result) -> None:
        """
        Adds one result. The same student cannot own two results
        of the same course in the same semester.
        """
        if self.find_result(result.student_id, result.course_id, result.semester) is not None:
            raise ResultManagerException(
                "Student " + result.student_id + " already has a result of "
                + result.course_id + " in " + result.semester + "."
            )
        #End if
        self._result_list.append(result)
    #End def

    def find_result(self, student_id: str, course_id: str, semester: str) -> Result:
        """Returns the one result that matches student, course and semester, or None."""
        student_id = student_id.strip().upper()
        course_id = course_id.strip().upper()
        semester = semester.strip().upper()
        for result in self._result_list:
            if (result.student_id == student_id
                    and result.course_id == course_id
                    and result.semester == semester):
                return result
            #End if
        #End for
        return None
    #End def

    def update_grade(self, student_id: str, course_id: str, semester: str,
                     grade_fe: float, grade_re: float) -> None:
        """Changes the two grades of one result."""
        result = self.find_result(student_id, course_id, semester)
        if result is None:
            raise ResultManagerException("That result does not exist.")
        #End if
        result.grade_fe = grade_fe
        result.grade_re = grade_re
    #End def

    def delete_result(self, student_id: str, course_id: str, semester: str) -> Result:
        """Removes one result and returns the removed object."""
        result = self.find_result(student_id, course_id, semester)
        if result is None:
            raise ResultManagerException("That result does not exist.")
        #End if
        self._result_list.remove(result)
        return result
    #End def

    def delete_result_of_student(self, student_id: str) -> int:
        """
        Removes every result of one student. The main program calls this
        after deleting a student so that no orphan result stays behind.
        """
        student_id = student_id.strip().upper()
        keep_list = []
        deleted_count = 0
        for result in self._result_list:
            if result.student_id == student_id:
                deleted_count = deleted_count + 1
            else:
                keep_list.append(result)
            #End if
        #End for
        self._result_list = keep_list
        return deleted_count
    #End def

    def get_result_list_of_student(self, student_id: str) -> list:
        """Returns every result of one student."""
        student_id = student_id.strip().upper()
        result_list = []
        for result in self._result_list:
            if result.student_id == student_id:
                result_list.append(result)
            #End if
        #End for
        return result_list
    #End def

    def get_all_result_list(self) -> list:
        """Returns every result of every student."""
        return list(self._result_list)
    #End def

    def calculate_gpa(self, student_id: str) -> float:
        """
        Returns the grade point average of one student, weighted by credits.
        Only results that already hold a grade are counted.
        Returns None when the student has no graded result yet.
        """
        result_list = self.get_result_list_of_student(student_id)
        total_point = 0.0
        total_credits = 0
        for result in result_list:
            best_grade = result.get_best_grade()
            if best_grade is None:
                continue
            #End if
            total_point = total_point + best_grade * result.credits
            total_credits = total_credits + result.credits
        #End for
        if total_credits == 0:
            return None
        #End if
        return round(total_point / total_credits, 2)
    #End def

    def count_passed_credits(self, student_id: str) -> int:
        """Returns how many credits one student has already passed."""
        total_credits = 0
        for result in self.get_result_list_of_student(student_id):
            if result.status == "Pass":
                total_credits = total_credits + result.credits
            #End if
        #End for
        return total_credits
    #End def

    def get_sorted_by_grade(self, student_id: str) -> list:
        """Returns the results of one student sorted from the highest grade down."""
        result_list = self.get_result_list_of_student(student_id)
        return sorted(
            result_list,
            key=lambda result: result.get_best_grade() if result.get_best_grade() is not None else -1,
            reverse=True
        )
    #End def

    def get_all_sorted_by_status(self) -> list:
        """
        Returns every result sorted by status, Pass rows first. Menu item 2.4.
        The key turns the status into a number so that Pass sorts before Fail
        and before the rows that have no grade yet.
        """
        order_dict = {"Pass": 0, "Fail": 1, "Not graded": 2}
        return sorted(self._result_list, key=lambda result: order_dict[result.status])
    #End def

    def get_pass_result_list(self) -> list:
        """Returns the results that are Pass. Menu item 2.5."""
        result_list = []
        for result in self._result_list:
            if result.status == "Pass":
                result_list.append(result)
            #End if
        #End for
        return result_list
    #End def

    def get_course_id_set(self) -> set:
        """Returns the set of every course that appears in the data."""
        course_id_set = set()
        for result in self._result_list:
            course_id_set.add(result.course_id)
        #End for
        return course_id_set
    #End def
#End class
