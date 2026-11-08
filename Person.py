# Person.py

class Person:
    """
    Base class for every person in the system.
    Student inherits from this class.
    """
    def __init__(self, full_name: str, date_of_birth: str, gender: str, phone: str, email: str):
        """
        Full constructor for Person.
        """
        # Protected attributes (conventionally private)
        self._full_name = full_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._phone = phone
        self._email = email
    #End def

    # --- Properties (Getters) ---
    @property
    def full_name(self) -> str:
        """Getter for full name."""
        return self._full_name
    #End def

    @property
    def date_of_birth(self) -> str:
        """Getter for date of birth."""
        return self._date_of_birth
    #End def

    @property
    def gender(self) -> str:
        """Getter for gender."""
        return self._gender
    #End def

    @property
    def phone(self) -> str:
        """Getter for phone number."""
        return self._phone
    #End def

    @property
    def email(self) -> str:
        """Getter for email."""
        return self._email
    #End def

    # --- Setters ---
    @full_name.setter
    def full_name(self, new_full_name: str):
        """Setter for full name."""
        self._full_name = new_full_name
    #End def

    @date_of_birth.setter
    def date_of_birth(self, new_date_of_birth: str):
        """Setter for date of birth."""
        self._date_of_birth = new_date_of_birth
    #End def

    @gender.setter
    def gender(self, new_gender: str):
        """Setter for gender."""
        self._gender = new_gender
    #End def

    @phone.setter
    def phone(self, new_phone: str):
        """Setter for phone number."""
        self._phone = new_phone
    #End def

    @email.setter
    def email(self, new_email: str):
        """Setter for email."""
        self._email = new_email
    #End def

    # --- Utility Methods ---
    def to_file_string(self) -> str:
        """
        Helper for File I/O. Child classes override this method.
        """
        return f"{self.full_name}|{self.date_of_birth}|{self.gender}|{self.phone}|{self.email}"
    #End def
#End class
