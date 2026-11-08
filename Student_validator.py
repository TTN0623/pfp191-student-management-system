# Student_validator.py

class StudentValidator:
    """
    Checks every value that belongs to a Student.
    This class is used only by the Student side of the program.
    """
    # Allowed values for the study status
    STATUS_TUPLE = ("Active", "Inactive", "Graduated")
    # Number of days of each month, used to check the date of birth
    DAYS_IN_MONTH_LIST = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def is_valid_student_id(self, student_id: str) -> bool:
        """
        A student ID starts with SE and ends with 5 or 6 digits, for example SE00001.
        """
        student_id = student_id.strip().upper()
        if len(student_id) != 7 and len(student_id) != 8:
            return False
        #End if
        if student_id[:2] != "SE":
            return False
        #End if
        return student_id[2:].isdigit()
    #End def

    def is_valid_class_name(self, class_name: str) -> bool:
        """
        A class name has letters and digits only, for example IA2102.
        """
        class_name = class_name.strip()
        if class_name == "":
            return False
        #End if
        return class_name.isalnum()
    #End def

    def is_valid_date_of_birth(self, date_of_birth: str) -> bool:
        """
        The date of birth has the form DD/MM/YYYY, for example 15/03/2005.
        """
        part_list = date_of_birth.strip().split("/")
        if len(part_list) != 3:
            return False
        #End if

        text_day, text_month, text_year = part_list
        if len(text_day) != 2 or len(text_month) != 2 or len(text_year) != 4:
            return False
        #End if
        if not (text_day.isdigit() and text_month.isdigit() and text_year.isdigit()):
            return False
        #End if

        day = int(text_day)
        month = int(text_month)
        year = int(text_year)
        if month < 1 or month > 12 or year < 1900:
            return False
        #End if

        # Work on a copy so that a leap year does not change the class attribute
        days_in_month_list = list(StudentValidator.DAYS_IN_MONTH_LIST)
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days_in_month_list[1] = 29
        #End if
        return 1 <= day <= days_in_month_list[month - 1]
    #End def

    def is_valid_gender(self, gender: str) -> bool:
        """Gender is Male or Female."""
        return gender.strip().lower() in ("male", "female")
    #End def

    def is_valid_phone(self, phone: str) -> bool:
        """A phone number has 10 digits and starts with 0."""
        phone = phone.strip()
        if len(phone) != 10:
            return False
        #End if
        if phone[0] != "0":
            return False
        #End if
        return phone.isdigit()
    #End def

    def is_valid_email(self, email: str) -> bool:
        """
        An email looks like name@domain and the domain holds a dot,
        for example an.nguyen@fpt.edu.vn
        """
        email = email.strip().lower()
        if email.count("@") != 1 or " " in email:
            return False
        #End if

        name_part, domain_part = email.split("@")
        if name_part == "":
            return False
        #End if
        if "." not in domain_part:
            return False
        #End if
        if domain_part[0] == "." or domain_part[-1] == ".":
            return False
        #End if
        return True
    #End def

    def is_valid_status(self, status: str) -> bool:
        """The study status is Active, Inactive or Graduated."""
        return status.strip().capitalize() in StudentValidator.STATUS_TUPLE
    #End def

    def is_valid_full_name(self, full_name: str) -> bool:
        """The full name cannot be empty and cannot hold the field separator."""
        full_name = full_name.strip()
        if full_name == "":
            return False
        #End if
        return "|" not in full_name
    #End def
#End class
