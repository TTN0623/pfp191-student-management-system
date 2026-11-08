# Result.py

class Result:
    """
    Represents the result of one student in one course.
    The status (Pass or Fail) is worked out from the grades, it is not stored.
    """
    # A student passes a course with a grade of 5 or more
    PASS_MARK = 5

    def __init__(self, student_id: str, course_id: str, course_name: str, semester: str,
                 credits: int, grade_fe: float, grade_re: float):
        """
        Full constructor for Result. grade_fe and grade_re may be None
        when the student has not taken that exam yet.
        """
        # Protected attributes (conventionally private)
        self._student_id = student_id.strip().upper()
        self._course_id = course_id.strip().upper()
        self._course_name = course_name
        self._semester = semester.strip().upper()
        self._credits = credits
        # The two grades go through the setters so that the range check runs here too
        self.grade_fe = grade_fe
        self.grade_re = grade_re
    #End def

    # --- Properties (Getters) ---
    @property
    def student_id(self) -> str:
        """Getter for the student ID. Read-only: there is no setter."""
        return self._student_id
    #End def

    @property
    def course_id(self) -> str:
        """Getter for the course ID. Read-only: there is no setter."""
        return self._course_id
    #End def

    @property
    def course_name(self) -> str:
        """Getter for the course name."""
        return self._course_name
    #End def

    @property
    def semester(self) -> str:
        """Getter for the semester."""
        return self._semester
    #End def

    @property
    def credits(self) -> int:
        """Getter for the number of credits."""
        return self._credits
    #End def

    @property
    def grade_fe(self) -> float:
        """Getter for the Final Exam grade."""
        return self._grade_fe
    #End def

    @property
    def grade_re(self) -> float:
        """Getter for the Re-exam grade."""
        return self._grade_re
    #End def

    @property
    def status(self) -> str:
        """
        Computed getter. Pass when FE >= 5, or when FE < 5 and RE >= 5.
        Not graded while the student has taken neither exam.
        Read-only: the value always follows the grades.
        """
        if self._grade_fe is None and self._grade_re is None:
            return "Not graded"
        #End if
        if self._grade_fe is not None and self._grade_fe >= Result.PASS_MARK:
            return "Pass"
        #End if
        if self._grade_re is not None and self._grade_re >= Result.PASS_MARK:
            return "Pass"
        #End if
        return "Fail"
    #End def

    # --- Setters ---
    @grade_fe.setter
    def grade_fe(self, new_grade_fe: float):
        """
        Setter for the final exam grade. None means the exam has not been taken.
        The range check lives here so that no wrong grade can enter the object.
        """
        self._grade_fe = Result.check_grade(new_grade_fe)
    #End def

    @grade_re.setter
    def grade_re(self, new_grade_re: float):
        """Setter for the re-exam grade. None means the exam has not been taken."""
        self._grade_re = Result.check_grade(new_grade_re)
    #End def

    @staticmethod
    def check_grade(new_grade: float) -> float:
        """Returns the grade when it runs from 0 to 10, and raises otherwise."""
        if new_grade is None:
            return None
        #End if
        new_grade = float(new_grade)
        if new_grade < 0 or new_grade > 10:
            raise ValueError("The grade must run from 0 to 10.")
        #End if
        return new_grade
    #End def

    # --- Utility Methods ---
    def get_best_grade(self) -> float:
        """Returns the grade that counts for the GPA, or None when there is none."""
        if self._grade_fe is None:
            return self._grade_re
        #End if
        if self._grade_re is None:
            return self._grade_fe
        #End if
        if self._grade_re > self._grade_fe:
            return self._grade_re
        #End if
        return self._grade_fe
    #End def

    def to_file_string(self) -> str:
        """
        Helper for File I/O. Returns one line of the data file, fields separated by |
        An empty field means the exam has not been taken.
        """
        text_fe = "" if self._grade_fe is None else str(self._grade_fe)
        text_re = "" if self._grade_re is None else str(self._grade_re)
        return (f"{self.student_id}|{self.course_id}|{self.course_name}|{self.semester}|"
                f"{self.credits}|{text_fe}|{text_re}")
    #End def

    def print_info(self, full_name: str = ""):
        """Prints one row of the result table."""
        text_fe = "-" if self._grade_fe is None else f"{self._grade_fe:.1f}"
        text_re = "-" if self._grade_re is None else f"{self._grade_re:.1f}"
        print(f"| {self.student_id:<8} | {full_name:<22} | {self.course_id:<8} | {self.course_name:<38} | "
              f"{self.semester:<8} | {self.credits:>7} | {text_fe:>4} | {text_re:>4} | {self.status:<10} |")
    #End def
#End class
