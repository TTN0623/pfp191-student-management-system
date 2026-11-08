# Student_manager.py
# VI: Lớp nghiệp vụ (manager) của phần Student: giữ dữ liệu trong bộ nhớ và áp dụng các luật.
# VI: Chứa StudentManagerException và StudentManager (thêm, sửa, xóa, tìm, lọc, sắp xếp, đếm).
# VI: Dùng Student (entity) và StudentFileHelper (đọc ghi file); không tự in hay tự nhập.
# VI: Được Main.py gọi, kết hợp với StudentConsoleIO để giao tiếp người dùng.
from models.Student import Student
from data_access.Student_file_helper import StudentFileHelper


# VI: Exception riêng của manager. Được ném khi vi phạm luật, ví dụ trùng mã hoặc không tìm thấy sinh viên.
class StudentManagerException(Exception):
    """Raised when a student action breaks a business rule."""
    pass
#End class


# VI: Class quản lý toàn bộ sinh viên. Dùng dict để tra theo mã sinh viên rất nhanh.
class StudentManager:
    """
    Holds every student in memory and runs the business rules on them.
    The data lives in a dictionary so that looking a student up by ID is fast.
    """

    # VI: Hàm khởi tạo: tạo file helper và một dict rỗng chưa có sinh viên nào.
    def __init__(self):
        self._file_helper = StudentFileHelper()
        # Key: student ID, value: the Student object
        self._student_dict = {}
    #End def

    # VI: Getter cho dict sinh viên, chỉ đọc (không có setter).
    @property
    def student_dict(self) -> dict:
        """Getter for the whole dictionary. Read-only: there is no setter."""
        return self._student_dict
    #End def

    # VI: Đọc file lên và xếp mọi sinh viên vào dict, khóa là mã sinh viên.
    # VI: Dict cũ bị thay mới hoàn toàn. Trả về số sinh viên đã đọc.
    def load_data(self) -> int:
        """Reads the data file and fills the dictionary. Returns how many students were read."""
        student_list = self._file_helper.load()
        self._student_dict = {}
        for student in student_list:
            self._student_dict[student.student_id] = student
        #End for
        return len(self._student_dict)
    #End def

    # VI: Ghi toàn bộ sinh viên trong dict ra file (đổi các giá trị của dict thành list trước).
    def save_data(self) -> None:
        """Writes the whole dictionary back to the data file."""
        self._file_helper.save(list(self._student_dict.values()))
    #End def

    # VI: Thêm một sinh viên. Ném StudentManagerException nếu mã sinh viên đã có.
    def add_student(self, student: Student) -> None:
        """Adds one student. The ID must not be used yet."""
        # VI: Luật nghiệp vụ: mã sinh viên là khóa nên không được trùng.
        if student.student_id in self._student_dict:
            raise StudentManagerException("Student ID " + student.student_id + " already exists.")
        #End if
        self._student_dict[student.student_id] = student
    #End def

    # VI: Tìm sinh viên theo mã. Trả về đối tượng Student, hoặc None nếu không có (không ném lỗi).
    def find_student_by_id(self, student_id: str) -> Student:
        """Returns the student with that ID, or None when nobody has it."""
        # VI: Chuẩn hóa mã (bỏ khoảng trắng, chữ hoa) rồi tra dict; get trả None khi thiếu khóa.
        return self._student_dict.get(student_id.strip().upper())
    #End def

    # VI: Sửa một cột của một sinh viên. Ném StudentManagerException nếu không có mã đó hoặc tên cột lạ.
    def update_student(self, student_id: str, field_name: str, new_value: str) -> None:
        """
        Changes one field of one student. The ID itself cannot be changed
        because it is the key of the dictionary.
        """
        student = self.find_student_by_id(student_id)
        if student is None:
            raise StudentManagerException("No student has the ID " + student_id + ".")
        #End if

        # VI: Gán qua setter của Student, nên giá trị sai vẫn bị setter chặn. Mã sinh viên không có nhánh nào ở đây.
        if field_name == "full_name":
            student.full_name = new_value
        elif field_name == "date_of_birth":
            student.date_of_birth = new_value
        elif field_name == "gender":
            student.gender = new_value
        elif field_name == "class_name":
            student.class_name = new_value
        elif field_name == "phone":
            student.phone = new_value
        elif field_name == "email":
            student.email = new_value
        elif field_name == "status":
            student.status = new_value
        else:
            raise StudentManagerException("The field " + field_name + " cannot be changed.")
        #End if
    #End def

    # VI: Xóa sinh viên theo mã và trả về đối tượng vừa xóa. Ném StudentManagerException nếu không có mã đó.
    def delete_student(self, student_id: str) -> Student:
        """Removes one student and returns the removed object."""
        student = self.find_student_by_id(student_id)
        if student is None:
            raise StudentManagerException("No student has the ID " + student_id + ".")
        #End if
        del self._student_dict[student.student_id]
        return student
    #End def

    # VI: Trả về mọi sinh viên dưới dạng list.
    def get_all_student_list(self) -> list:
        """Returns every student as a list."""
        return list(self._student_dict.values())
    #End def

    # VI: Tìm theo tên: sinh viên nào có tên chứa từ khóa (không phân biệt hoa thường) thì vào list kết quả.
    def search_by_name(self, keyword: str) -> list:
        """Returns every student whose name holds the keyword, ignoring upper or lower case."""
        keyword = keyword.strip().lower()
        student_list = []
        for student in self._student_dict.values():
            if keyword in student.full_name.lower():
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    # VI: Lọc theo lớp: lấy những sinh viên có class_name đúng bằng tên lớp đã chuẩn hóa.
    def search_by_class(self, class_name: str) -> list:
        """Returns every student of one class."""
        class_name = class_name.strip().upper()
        student_list = []
        for student in self._student_dict.values():
            if student.class_name == class_name:
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    # VI: Lọc theo trạng thái học (Active, Inactive, Graduated). Dùng cho mục menu 1.3.
    def search_by_status(self, status: str) -> list:
        """Returns every student of one study status. Menu item 1.3."""
        status = status.strip().capitalize()
        student_list = []
        for student in self._student_dict.values():
            if student.status == status:
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    # VI: Lấy sinh viên đang học (is_active của Student trả True). Dùng cho mục menu 1.4.
    def get_active_student_list(self) -> list:
        """Returns every student who is still studying. Menu item 1.4."""
        student_list = []
        for student in self._student_dict.values():
            if student.is_active():
                student_list.append(student)
            #End if
        #End for
        return student_list
    #End def

    # VI: Trả về list đã sắp xếp theo họ tên từ A đến Z. key chuyển sang chữ thường để so sánh công bằng.
    def get_sorted_by_name(self) -> list:
        """Returns every student sorted by full name from A to Z."""
        return sorted(self._student_dict.values(), key=lambda student: student.full_name.lower())
    #End def

    # VI: Trả về list đã sắp xếp theo mã sinh viên.
    def get_sorted_by_id(self) -> list:
        """Returns every student sorted by student ID."""
        return sorted(self._student_dict.values(), key=lambda student: student.student_id)
    #End def

    # VI: Đếm số sinh viên theo từng trạng thái. Trả về dict {trạng thái: số lượng}.
    def count_by_status(self) -> dict:
        """Counts how many students stand in each study status."""
        count_dict = {}
        # VI: Cho mọi trạng thái hợp lệ bắt đầu bằng 0 để trạng thái chưa có ai vẫn hiện ra số 0.
        for status in Student.STATUS_TUPLE:
            count_dict[status] = 0
        #End for
        for student in self._student_dict.values():
            # VI: get(..., 0) lấy số đếm hiện tại rồi cộng thêm 1 cho sinh viên này.
            count_dict[student.status] = count_dict.get(student.status, 0) + 1
        #End for
        return count_dict
    #End def

    # VI: Trả về set các lớp có trong dữ liệu. Set tự loại bỏ tên lớp trùng.
    def get_class_name_set(self) -> set:
        """Returns the set of every class that appears in the data."""
        class_name_set = set()
        for student in self._student_dict.values():
            class_name_set.add(student.class_name)
        #End for
        return class_name_set
    #End def
#End class
