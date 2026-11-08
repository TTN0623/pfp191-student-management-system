# Result_io.py
from Result import Result
from Result_validator import ResultValidator


class ResultConsoleIO:
    """
    Talks to the user about study results: menu, input, tables.
    No business rule and no file work lives here.
    """

    def __init__(self):
        self._validator = ResultValidator()
    #End def

    # --- Menu ---
    def show_result_menu(self) -> None:
        """Prints the result menu."""
        print("\n--- RESULT MENU ---")
        print("2.1 Add a course grade")
        print("2.2 Update a grade")
        print("2.3 Search enrollments by student ID")
        print("2.4 Display results sorted by status")
        print("2.5 Display students with Pass")
        print("2.6 Calculate the GPA of one student")
        print("7.  Delete a result")
        print("0.  Back to the main menu")
    #End def

    # --- Reading one field ---
    def read_course_id(self) -> str:
        """Keeps asking until the course ID holds letters and digits only."""
        while True:
            value = input("Course ID (example PFP191): ").strip().upper()
            if self._validator.is_valid_course_id(value):
                return value
            #End if
            print("The course ID holds letters and digits only.")
        #End while
    #End def

    def read_course_name(self) -> str:
        """Keeps asking until the course name is not empty."""
        while True:
            value = input("Course name: ").strip()
            if self._validator.is_valid_course_name(value):
                return value
            #End if
            print("The course name cannot be empty and cannot hold the character |")
        #End while
    #End def

    def read_semester(self) -> str:
        """Keeps asking until the semester has two letters and two digits."""
        while True:
            value = input("Semester (example FA26): ").strip().upper()
            if self._validator.is_valid_semester(value):
                return value
            #End if
            print("Wrong format. Example: FA26, SP27, SU27")
        #End while
    #End def

    def read_credits(self) -> int:
        """Keeps asking until the number of credits runs from 1 to 4."""
        while True:
            value = input("Credits (1 to 4): ").strip()
            if value.isdigit() and self._validator.is_valid_credits(int(value)):
                return int(value)
            #End if
            print("Please type a number from 1 to 4.")
        #End while
    #End def

    def read_grade(self, prompt: str) -> float:
        """
        Reads one grade from 0 to 10.
        An empty line means the student has not taken that exam, so it returns None.
        """
        while True:
            value = input(prompt).strip()
            if value == "":
                return None
            #End if
            try:
                grade = float(value)
            except ValueError:
                print("Please type a number, or leave the line empty.")
                continue
            #End try
            if self._validator.is_valid_grade(grade):
                return grade
            #End if
            print("The grade runs from 0 to 10.")
        #End while
    #End def

    def read_menu_choice(self, min_choice: int, max_choice: int) -> int:
        """Keeps asking until the user types a number inside the menu range."""
        while True:
            value = input("Your choice: ").strip()
            if value.isdigit() and min_choice <= int(value) <= max_choice:
                return int(value)
            #End if
            print("Please type a number from " + str(min_choice) + " to " + str(max_choice) + ".")
        #End while
    #End def

    # --- Building one object ---
    def read_new_result(self, student_id: str) -> Result:
        """Asks for every field of one result of a known student."""
        print("\n--- NEW RESULT FOR " + student_id + " ---")
        course_id = self.read_course_id()
        course_name = self.read_course_name()
        semester = self.read_semester()
        credits = self.read_credits()
        grade_fe = self.read_grade("Final exam grade (leave empty when not taken): ")
        grade_re = None
        if self._validator.can_take_re_exam(grade_fe):
            grade_re = self.read_grade("Re-exam grade (leave empty when not taken): ")
        #End if
        return Result(student_id, course_id, course_name, semester, credits, grade_fe, grade_re)
    #End def

    def read_grade_pair(self) -> tuple:
        """
        Reads the two grades of an existing result.
        The re-exam grade is asked only when the final exam has failed.
        """
        grade_fe = self.read_grade("New final exam grade (leave empty when not taken): ")
        grade_re = None
        if self._validator.can_take_re_exam(grade_fe):
            grade_re = self.read_grade("New re-exam grade (leave empty when not taken): ")
        #End if
        return (grade_fe, grade_re)
    #End def

    # --- Printing ---
    def display_result_list(self, result_list: list, name_dict: dict = None) -> None:
        """
        Prints a table of results. name_dict maps a student ID to a full name
        so that the table can show the name beside the ID.
        """
        if len(result_list) == 0:
            print("No result to show.")
            return
        #End if
        if name_dict is None:
            name_dict = {}
        #End if
        print("\n" + "-" * 137)
        print(f"| {'ID':<8} | {'FULL NAME':<22} | {'COURSE':<8} | {'COURSE NAME':<38} | "
              f"{'SEMESTER':<8} | {'CREDITS':>7} | {'FE':>4} | {'RE':>4} | {'STATUS':<10} |")
        print("-" * 137)
        for result in result_list:
            result.print_info(name_dict.get(result.student_id, ""))
        #End for
        print("-" * 137)
        print("Total: " + str(len(result_list)) + " result(s)")
    #End def

    def display_gpa(self, student_id: str, full_name: str, gpa: float, passed_credits: int) -> None:
        """Prints the GPA and the passed credits of one student."""
        print("\n--- ACADEMIC SUMMARY ---")
        print("Student  : " + student_id + " - " + full_name)
        if gpa is None:
            print("GPA      : no graded result yet")
        else:
            print("GPA      : " + str(gpa) + " / 10")
        #End if
        print("Passed credits: " + str(passed_credits))
    #End def

    def show_message(self, message: str) -> None:
        """Prints one line of feedback to the user."""
        print(message)
    #End def
#End class
