# Student.py
from Person import Person  # Import the Person class

class Student(Person):
    """
    Represents one student. Inherits the personal details from Person
    and adds the student ID, the class name and the study status.
    """
    # Allowed values for the study status
    STATUS_TUPLE = ("Active", "Inactive", "Graduated")

    def __init__(self, student_id: str, full_name: str, date_of_birth: str, gender: str,
                 class_name: str, phone: str, email: str, status: str):
        """
        Full constructor for Student. Calls the constructor of Person first.
        """
        super().__init__(full_name, date_of_birth, gender, phone, email)

        # Protected attributes (conventionally private)
        self._student_id = student_id.strip().upper()
        self._class_name = class_name.strip().upper()
        # The status goes through the setter so that the check runs here too
        self.status = status
    #End def

    # --- Properties (Getters) ---
    @property
    def student_id(self) -> str:
        """Getter for the student ID. Read-only: there is no setter."""
        return self._student_id
    #End def

    @property
    def class_name(self) -> str:
        """Getter for the class name."""
        return self._class_name
    #End def

    @property
    def status(self) -> str:
        """Getter for the study status."""
        return self._status
    #End def

    # --- Setters ---
    @class_name.setter
    def class_name(self, new_class_name: str):
        """Setter for the class name, used by StudentManager update logic."""
        self._class_name = new_class_name.strip().upper()
    #End def

    @status.setter
    def status(self, new_status: str):
        """
        Setter for the study status. The check lives here as well so that no
        code anywhere can put a wrong value inside the object.
        """
        new_status = new_status.strip().capitalize()
        if new_status not in Student.STATUS_TUPLE:
            raise ValueError("The status must be Active, Inactive or Graduated.")
        #End if
        self._status = new_status
    #End def

    # --- Utility Methods ---
    def is_active(self) -> bool:
        """Returns True when the student is still studying."""
        return self._status == "Active"
    #End def

    def to_file_string(self) -> str:
        """
        Helper for File I/O. Overrides Person.to_file_string().
        Returns one line of the data file, fields separated by |
        """
        return (f"{self.student_id}|{self.full_name}|{self.date_of_birth}|{self.gender}|"
                f"{self.class_name}|{self.phone}|{self.email}|{self.status}")
    #End def

    def print_info(self):
        """Prints one row of the student table."""
        print(f"| {self.student_id:<8} | {self.full_name:<22} | {self.date_of_birth:<10} | "
              f"{self.gender:<6} | {self.class_name:<8} | {self.phone:<11} | {self.email:<26} | {self.status:<9} |")
    #End def
#End class
