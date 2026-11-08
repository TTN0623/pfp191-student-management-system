# Person.py
# VI: Thuộc lớp Entity (đối tượng dữ liệu) trong mô hình, là class cha.
# VI: Chứa class Person: thông tin cá nhân chung của một người.
# VI: Student.py import file này và kế thừa từ Person.

# VI: Class cha của mọi người trong hệ thống, Student kế thừa từ đây.
# VI: Chỉ giữ họ tên, ngày sinh, giới tính, số điện thoại, email.
class Person:
    """
    Base class for every person in the system.
    Student inherits from this class.
    """
    # VI: Constructor: nhận 5 thông tin cá nhân và gán vào thuộc tính. Chưa kiểm tra hợp lệ ở đây.
    def __init__(self, full_name: str, date_of_birth: str, gender: str, phone: str, email: str):
        """
        Full constructor for Person.
        """
        # VI: Dấu gạch dưới đầu tên (_) là quy ước: bên ngoài không đụng trực tiếp mà đi qua property.
        # Protected attributes (conventionally private)
        self._full_name = full_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._phone = phone
        self._email = email
    #End def

    # --- Properties (Getters) ---
    # VI: Getter: đọc họ tên bằng person.full_name, không cần gọi như hàm.
    @property
    def full_name(self) -> str:
        """Getter for full name."""
        return self._full_name
    #End def

    # VI: Getter: trả về ngày sinh (chuỗi DD/MM/YYYY).
    @property
    def date_of_birth(self) -> str:
        """Getter for date of birth."""
        return self._date_of_birth
    #End def

    # VI: Getter: trả về giới tính.
    @property
    def gender(self) -> str:
        """Getter for gender."""
        return self._gender
    #End def

    # VI: Getter: trả về số điện thoại.
    @property
    def phone(self) -> str:
        """Getter for phone number."""
        return self._phone
    #End def

    # VI: Getter: trả về email.
    @property
    def email(self) -> str:
        """Getter for email."""
        return self._email
    #End def

    # --- Setters ---
    # VI: Setter: gán họ tên mới bằng person.full_name = '...'. Không kiểm tra, việc kiểm tra do validator lo.
    @full_name.setter
    def full_name(self, new_full_name: str):
        """Setter for full name."""
        self._full_name = new_full_name
    #End def

    # VI: Setter: gán ngày sinh mới.
    @date_of_birth.setter
    def date_of_birth(self, new_date_of_birth: str):
        """Setter for date of birth."""
        self._date_of_birth = new_date_of_birth
    #End def

    # VI: Setter: gán giới tính mới.
    @gender.setter
    def gender(self, new_gender: str):
        """Setter for gender."""
        self._gender = new_gender
    #End def

    # VI: Setter: gán số điện thoại mới.
    @phone.setter
    def phone(self, new_phone: str):
        """Setter for phone number."""
        self._phone = new_phone
    #End def

    # VI: Setter: gán email mới.
    @email.setter
    def email(self, new_email: str):
        """Setter for email."""
        self._email = new_email
    #End def

    # --- Utility Methods ---
    # VI: Ghép 5 thông tin thành một dòng, ngăn cách bằng dấu |, để ghi ra file.
    # VI: Student ghi đè (override) hàm này để thêm mã SV, lớp và trạng thái.
    def to_file_string(self) -> str:
        """
        Helper for File I/O. Child classes override this method.
        """
        return f"{self.full_name}|{self.date_of_birth}|{self.gender}|{self.phone}|{self.email}"
    #End def
#End class
