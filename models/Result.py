# Result.py
# VI: Lớp entity (dữ liệu) của phần Result: một dòng điểm của một sinh viên ở một môn.
# VI: Chứa class Result, lưu mã SV, mã môn, tên môn, kỳ học, số tín chỉ, điểm FE và điểm RE.
# VI: Được Result_manager.py, Result_io.py và Result_file_helper.py dùng.
# VI: Trạng thái Pass/Fail không lưu mà tính ra từ điểm.

# VI: Class đại diện kết quả học một môn của một sinh viên. Các thuộc tính để dạng protected (có dấu gạch dưới) và truy cập qua property.
class Result:
    """
    Represents the result of one student in one course.
    The status (Pass or Fail) is worked out from the grades, it is not stored.
    """
    # A student passes a course with a grade of 5 or more
    # VI: Hằng số điểm đạt: từ 5 trở lên là qua môn.
    PASS_MARK = 5

    # VI: Hàm khởi tạo đầy đủ. Mã và kỳ học được bỏ khoảng trắng và đổi chữ hoa. grade_fe, grade_re có thể là None.
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
        # VI: Gán qua setter (self.grade_fe) chứ không gán thẳng _grade_fe, để luôn chạy kiểm tra khoảng 0 đến 10.
        # The two grades go through the setters so that the range check runs here too
        self.grade_fe = grade_fe
        self.grade_re = grade_re
    #End def

    # --- Properties (Getters) ---
    # VI: Getter mã sinh viên, chỉ đọc.
    @property
    def student_id(self) -> str:
        """Getter for the student ID. Read-only: there is no setter."""
        return self._student_id
    #End def

    # VI: Getter mã môn, chỉ đọc.
    @property
    def course_id(self) -> str:
        """Getter for the course ID. Read-only: there is no setter."""
        return self._course_id
    #End def

    # VI: Getter tên môn.
    @property
    def course_name(self) -> str:
        """Getter for the course name."""
        return self._course_name
    #End def

    # VI: Getter kỳ học.
    @property
    def semester(self) -> str:
        """Getter for the semester."""
        return self._semester
    #End def

    # VI: Getter số tín chỉ.
    @property
    def credits(self) -> int:
        """Getter for the number of credits."""
        return self._credits
    #End def

    # VI: Getter điểm thi cuối kỳ FE (Final Exam). None nghĩa là chưa thi.
    @property
    def grade_fe(self) -> float:
        """Getter for the Final Exam grade."""
        return self._grade_fe
    #End def

    # VI: Getter điểm thi lại RE (Re-exam). None nghĩa là chưa thi lại.
    @property
    def grade_re(self) -> float:
        """Getter for the Re-exam grade."""
        return self._grade_re
    #End def

    # VI: Getter tính toán, trả về "Pass", "Fail" hoặc "Not graded". Không có setter vì luôn đi theo điểm.
    @property
    def status(self) -> str:
        """
        Computed getter. Pass when FE >= 5, or when FE < 5 and RE >= 5.
        Not graded while the student has taken neither exam.
        Read-only: the value always follows the grades.
        """
        # VI: Chưa có điểm nào: chưa chấm.
        if self._grade_fe is None and self._grade_re is None:
            return "Not graded"
        #End if
        # VI: FE đạt thì Pass ngay, không cần xét RE.
        if self._grade_fe is not None and self._grade_fe >= Result.PASS_MARK:
            return "Pass"
        #End if
        # VI: FE chưa đạt (hoặc chưa thi) nhưng RE đạt thì vẫn Pass.
        if self._grade_re is not None and self._grade_re >= Result.PASS_MARK:
            return "Pass"
        #End if
        # VI: Có điểm nhưng không điểm nào đạt thì Fail.
        return "Fail"
    #End def

    # --- Setters ---
    # VI: Setter điểm FE. Gọi check_grade nên điểm ngoài đoạn 0 đến 10 sẽ ném ValueError.
    @grade_fe.setter
    def grade_fe(self, new_grade_fe: float):
        """
        Setter for the final exam grade. None means the exam has not been taken.
        The range check lives here so that no wrong grade can enter the object.
        """
        self._grade_fe = Result.check_grade(new_grade_fe)
    #End def

    # VI: Setter điểm RE, cũng kiểm tra bằng check_grade.
    @grade_re.setter
    def grade_re(self, new_grade_re: float):
        """Setter for the re-exam grade. None means the exam has not been taken."""
        self._grade_re = Result.check_grade(new_grade_re)
    #End def

    # VI: Hàm tĩnh (không cần self): kiểm tra điểm. Trả về điểm dạng float, None giữ nguyên, ngoài 0 đến 10 thì ném ValueError.
    @staticmethod
    def check_grade(new_grade: float) -> float:
        """Returns the grade when it runs from 0 to 10, and raises otherwise."""
        if new_grade is None:
            return None
        #End if
        # VI: Đổi sang float để chuỗi như "7.5" cũng dùng được.
        new_grade = float(new_grade)
        if new_grade < 0 or new_grade > 10:
            raise ValueError("The grade must run from 0 to 10.")
        #End if
        return new_grade
    #End def

    # --- Utility Methods ---
    # VI: Điểm tính vào GPA: lấy điểm cao hơn giữa FE và RE. Chỉ có một điểm thì lấy điểm đó, không có thì trả None.
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

    # VI: Đổi đối tượng thành một dòng chữ để ghi file, các cột ngăn bằng |. Điểm chưa thi ghi thành ô trống.
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

    # VI: Tạo một dòng của bảng kết quả. Họ tên không nằm trong Result nên được truyền vào (mặc định rỗng). Điểm None in dấu -.
    def format_row(self, full_name: str = "") -> str:
        """Returns one row of the result table."""
        text_fe = "-" if self._grade_fe is None else f"{self._grade_fe:.1f}"
        text_re = "-" if self._grade_re is None else f"{self._grade_re:.1f}"
        return (f"| {self.student_id:<8} | {full_name:<22} | {self.course_id:<8} | {self.course_name:<38} | "
                f"{self.semester:<8} | {self.credits:>7} | {text_fe:>4} | {text_re:>4} | {self.status:<10} |")
    #End def

    # VI: __str__ được gọi khi print(result) hoặc str(result): một dòng bảng, cột họ tên để trống.
    def __str__(self) -> str:
        """Readable one-line text, used by print() and str()."""
        return self.format_row()
    #End def

    # VI: In một dòng của bảng kết quả kèm họ tên sinh viên.
    def print_info(self, full_name: str = ""):
        """Prints one row of the result table."""
        print(self.format_row(full_name))
    #End def
#End class
