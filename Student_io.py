# Student_io.py
from Student import Student
from Student_validator import StudentValidator


class StudentConsoleIO:
    """
    Talks to the user about students: shows the menu, reads the input,
    prints the tables. No business rule and no file work lives here.
    """

    def __init__(self):
        self._validator = StudentValidator()
    #End def

    # --- Menu ---
    def show_student_menu(self) -> None:
        """Prints the student menu."""
        print("\n--- STUDENT MENU ---")
        print("1.1 Add a new student")
        print("1.2 Update student information")
        print("1.3 Filter students by class or status")
        print("1.4 Display active students")
        print("5.  Display every student")
        print("6.  Search a student by name")
        print("7.  Delete a student")
        print("8.  Count students by status")
        print("0.  Back to the main menu")
    #End def

    def read_filter_choice(self) -> int:
        """Asks whether the user wants to filter by class or by status. Menu item 1.3."""
        print("1. By class   2. By status")
        return self.read_menu_choice(1, 2)
    #End def

    # --- Reading one field ---
    def read_student_id(self, prompt: str = "Student ID (SE + 5 or 6 digits): ") -> str:
        """Keeps asking until the user types a student ID of the right shape."""
        while True:
            value = input(prompt).strip().upper()
            if self._validator.is_valid_student_id(value):
                return value
            #End if
            print("Wrong format. Example: SE00001")
        #End while
    #End def

    def read_full_name(self) -> str:
        """Keeps asking until the full name is not empty."""
        while True:
            value = input("Full name: ").strip()
            if self._validator.is_valid_full_name(value):
                return value
            #End if
            print("The name cannot be empty and cannot hold the character |")
        #End while
    #End def

    def read_date_of_birth(self) -> str:
        """Keeps asking until the date of birth has the form DD/MM/YYYY."""
        while True:
            value = input("Date of birth (DD/MM/YYYY): ").strip()
            if self._validator.is_valid_date_of_birth(value):
                return value
            #End if
            print("Wrong format. Example: 15/03/2005")
        #End while
    #End def

    def read_gender(self) -> str:
        """Keeps asking until the user types Male or Female."""
        while True:
            value = input("Gender (Male / Female): ").strip()
            if self._validator.is_valid_gender(value):
                return value.capitalize()
            #End if
            print("Please type Male or Female.")
        #End while
    #End def

    def read_class_name(self) -> str:
        """Keeps asking until the class name holds letters and digits only."""
        while True:
            value = input("Class (example IA2102): ").strip().upper()
            if self._validator.is_valid_class_name(value):
                return value
            #End if
            print("The class name holds letters and digits only.")
        #End while
    #End def

    def read_phone(self) -> str:
        """Keeps asking until the phone number has 10 digits and starts with 0."""
        while True:
            value = input("Phone (10 digits, starts with 0): ").strip()
            if self._validator.is_valid_phone(value):
                return value
            #End if
            print("Wrong format. Example: 0901234567")
        #End while
    #End def

    def read_email(self) -> str:
        """Keeps asking until the email holds one @ and a dot in the domain."""
        while True:
            value = input("Email: ").strip().lower()
            if self._validator.is_valid_email(value):
                return value
            #End if
            print("Wrong format. Example: an.nguyen@fpt.edu.vn")
        #End while
    #End def

    def read_status(self) -> str:
        """Keeps asking until the status is Active, Inactive or Graduated."""
        while True:
            value = input("Status (Active / Inactive / Graduated): ").strip()
            if self._validator.is_valid_status(value):
                return value.capitalize()
            #End if
            print("Please type Active, Inactive or Graduated.")
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

    def read_text(self, prompt: str) -> str:
        """Reads one line of free text, used for a search keyword."""
        return input(prompt).strip()
    #End def

    # --- Building one object ---
    def read_new_student(self) -> Student:
        """Asks for every field and returns a new Student object."""
        print("\n--- NEW STUDENT ---")
        return Student(
            student_id=self.read_student_id(),
            full_name=self.read_full_name(),
            date_of_birth=self.read_date_of_birth(),
            gender=self.read_gender(),
            class_name=self.read_class_name(),
            phone=self.read_phone(),
            email=self.read_email(),
            status=self.read_status()
        )
    #End def

    def read_field_to_update(self) -> str:
        """Asks which field the user wants to change and returns its name."""
        field_name_list = ["full_name", "date_of_birth", "gender",
                           "class_name", "phone", "email", "status"]
        print("\nWhich field do you want to change?")
        for index in range(len(field_name_list)):
            print(str(index + 1) + ". " + field_name_list[index])
        #End for
        choice = self.read_menu_choice(1, len(field_name_list))
        return field_name_list[choice - 1]
    #End def

    def read_new_value(self, field_name: str) -> str:
        """Reads the new value of one field, with the check of that field."""
        if field_name == "full_name":
            return self.read_full_name()
        elif field_name == "date_of_birth":
            return self.read_date_of_birth()
        elif field_name == "gender":
            return self.read_gender()
        elif field_name == "class_name":
            return self.read_class_name()
        elif field_name == "phone":
            return self.read_phone()
        elif field_name == "email":
            return self.read_email()
        else:
            return self.read_status()
        #End if
    #End def

    # --- Printing ---
    def display_student_list(self, student_list: list) -> None:
        """Prints a table of students, or a note when the list is empty."""
        if len(student_list) == 0:
            print("No student to show.")
            return
        #End if
        print("\n" + "-" * 125)
        print(f"| {'ID':<8} | {'FULL NAME':<22} | {'BIRTH':<10} | {'GENDER':<6} | "
              f"{'CLASS':<8} | {'PHONE':<11} | {'EMAIL':<26} | {'STATUS':<9} |")
        print("-" * 125)
        for student in student_list:
            student.print_info()
        #End for
        print("-" * 125)
        print("Total: " + str(len(student_list)) + " student(s)")
    #End def

    def display_count_by_status(self, count_dict: dict) -> None:
        """Prints how many students stand in each status."""
        print("\n--- STUDENTS BY STATUS ---")
        for status in count_dict:
            print(f"{status:<12}: {count_dict[status]}")
        #End for
    #End def

    def show_message(self, message: str) -> None:
        """Prints one line of feedback to the user."""
        print(message)
    #End def
#End class
