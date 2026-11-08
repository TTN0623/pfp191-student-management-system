# Student.py
# VI: Thuộc lớp Entity (đối tượng dữ liệu) trong mô hình.
# VI: Chứa class Student, kế thừa Person, thêm mã SV, lớp, trạng thái học.
# VI: Được dùng bởi Student_manager, Student_io và Student_file_helper.
from Person import Person  # Import the Person class

# VI: Một sinh viên. Kế thừa thông tin cá nhân từ Person, thêm mã SV, tên lớp, trạng thái học.
class Student(Person):
    """
    Represents one student. Inherits the personal details from Person
    and adds the student ID, the class name and the study status.
    """
    # Allowed values for the study status
    # VI: Tuple hằng số: chỉ 3 giá trị trạng thái này được chấp nhận.
    STATUS_TUPLE = ("Active", "Inactive", "Graduated")

    # VI: Constructor: gọi constructor của Person cho thông tin cá nhân, rồi gán phần riêng của Student.
    # VI: Mã SV và tên lớp được cắt khoảng trắng và đổi sang chữ hoa. Trạng thái sai thì ném ValueError (qua setter).
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
        # VI: Gán qua setter (không phải self._status) để luôn chạy bước kiểm tra trạng thái.
        self.status = status
    #End def

    # --- Properties (Getters) ---
    # VI: Getter của mã SV. Không có setter nên mã SV chỉ đọc, không đổi được sau khi tạo.
    @property
    def student_id(self) -> str:
        """Getter for the student ID. Read-only: there is no setter."""
        return self._student_id
    #End def

    # VI: Getter: trả về tên lớp (đã viết hoa).
    @property
    def class_name(self) -> str:
        """Getter for the class name."""
        return self._class_name
    #End def

    # VI: Getter: trả về trạng thái học.
    @property
    def status(self) -> str:
        """Getter for the study status."""
        return self._status
    #End def

    # --- Setters ---
    # VI: Setter: đổi tên lớp, cũng cắt khoảng trắng và viết hoa. StudentManager gọi khi cập nhật.
    @class_name.setter
    def class_name(self, new_class_name: str):
        """Setter for the class name, used by StudentManager update logic."""
        self._class_name = new_class_name.strip().upper()
    #End def

    # VI: Setter: chuẩn hóa chữ (vd 'active' thành 'Active') rồi kiểm tra có nằm trong STATUS_TUPLE không.
    # VI: Không hợp lệ thì ném ValueError.
    @status.setter
    def status(self, new_status: str):
        """
        Setter for the study status. The check lives here as well so that no
        code anywhere can put a wrong value inside the object.
        """
        new_status = new_status.strip().capitalize()
        # VI: Giá trị lạ bị chặn ngay tại đây, nên object Student không bao giờ chứa trạng thái sai.
        if new_status not in Student.STATUS_TUPLE:
            raise ValueError("The status must be Active, Inactive or Graduated.")
        #End if
        self._status = new_status
    #End def

    # --- Utility Methods ---
    # VI: Trả về True nếu sinh viên đang học (trạng thái Active), ngược lại False.
    def is_active(self) -> bool:
        """Returns True when the student is still studying."""
        return self._status == "Active"
    #End def

    # VI: Ghi đè Person.to_file_string(): trả về 1 dòng 8 trường ngăn cách bằng |, đúng thứ tự file dữ liệu.
    def to_file_string(self) -> str:
        """
        Helper for File I/O. Overrides Person.to_file_string().
        Returns one line of the data file, fields separated by |
        """
        return (f"{self.student_id}|{self.full_name}|{self.date_of_birth}|{self.gender}|"
                f"{self.class_name}|{self.phone}|{self.email}|{self.status}")
    #End def

    # VI: In một dòng bảng sinh viên ra màn hình. Dấu :<8, :<22... là căn lề trái theo độ rộng cột.
    def print_info(self):
        """Prints one row of the student table."""
        print(f"| {self.student_id:<8} | {self.full_name:<22} | {self.date_of_birth:<10} | "
              f"{self.gender:<6} | {self.class_name:<8} | {self.phone:<11} | {self.email:<26} | {self.status:<9} |")
    #End def
#End class
