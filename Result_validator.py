# Result_validator.py

class ResultValidator:
    """
    Checks every value that belongs to a Result.
    This class is used only by the Result side of the program.
    """
    # A course is worth 1 to 4 credits
    CREDITS_TUPLE = (1, 2, 3, 4)
    # Grades run from 0 to 10
    MIN_GRADE = 0
    MAX_GRADE = 10

    def is_valid_course_id(self, course_id: str) -> bool:
        """
        A course ID has letters and digits only, for example PFP191.
        """
        course_id = course_id.strip()
        if course_id == "":
            return False
        #End if
        return course_id.isalnum()
    #End def

    def is_valid_course_name(self, course_name: str) -> bool:
        """The course name cannot be empty and cannot hold the field separator."""
        course_name = course_name.strip()
        if course_name == "":
            return False
        #End if
        return "|" not in course_name
    #End def

    def is_valid_semester(self, semester: str) -> bool:
        """
        A semester has two letters and two digits, for example FA26.
        """
        semester = semester.strip().upper()
        if len(semester) != 4:
            return False
        #End if
        return semester[:2].isalpha() and semester[2:].isdigit()
    #End def

    def is_valid_credits(self, credits: int) -> bool:
        """A course is worth 1 to 4 credits."""
        return credits in ResultValidator.CREDITS_TUPLE
    #End def

    def is_valid_grade(self, grade: float) -> bool:
        """
        A grade runs from 0 to 10. None is allowed and means
        the student has not taken that exam yet.
        """
        if grade is None:
            return True
        #End if
        return ResultValidator.MIN_GRADE <= grade <= ResultValidator.MAX_GRADE
    #End def

    def can_take_re_exam(self, grade_fe: float) -> bool:
        """
        A student takes the re-exam only after failing the final exam,
        so the RE grade is accepted only when FE is below the pass mark.
        """
        if grade_fe is None:
            return False
        #End if
        return grade_fe < 5
    #End def
#End class
