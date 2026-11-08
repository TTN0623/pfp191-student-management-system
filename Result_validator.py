# Result_validator.py
# VI: Lớp kiểm tra (validator) của phần Result: chỉ trả True hoặc False, không ném lỗi, không nhập xuất.
# VI: Chứa class ResultValidator, kiểm tra mã môn, tên môn, kỳ học, tín chỉ, điểm và luật thi lại.
# VI: Được Result_io.py gọi trước khi tạo đối tượng Result; Result tự kiểm thêm khoảng điểm trong setter.

# VI: Class gom các hàm kiểm tra giá trị của Result. Phần Student có validator riêng, không dùng chung.
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

    # VI: Mã môn hợp lệ khi không rỗng và chỉ gồm chữ và số (isalnum), ví dụ PFP191.
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

    # VI: Tên môn hợp lệ khi không rỗng và không chứa ký tự |, vì | là dấu ngăn cách cột trong file dữ liệu.
    def is_valid_course_name(self, course_name: str) -> bool:
        """The course name cannot be empty and cannot hold the field separator."""
        course_name = course_name.strip()
        if course_name == "":
            return False
        #End if
        return "|" not in course_name
    #End def

    # VI: Kỳ học hợp lệ khi đúng 4 ký tự: 2 chữ cái rồi 2 chữ số, ví dụ FA26.
    def is_valid_semester(self, semester: str) -> bool:
        """
        A semester has two letters and two digits, for example FA26.
        """
        semester = semester.strip().upper()
        # VI: Sai độ dài thì loại ngay, chưa cần xét từng ký tự.
        if len(semester) != 4:
            return False
        #End if
        return semester[:2].isalpha() and semester[2:].isdigit()
    #End def

    # VI: Số tín chỉ hợp lệ khi nằm trong CREDITS_TUPLE (1 đến 4).
    def is_valid_credits(self, credits: int) -> bool:
        """A course is worth 1 to 4 credits."""
        return credits in ResultValidator.CREDITS_TUPLE
    #End def

    # VI: Điểm hợp lệ khi từ 0 đến 10. None cũng hợp lệ vì nghĩa là chưa thi.
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

    # VI: Luật nghiệp vụ: chỉ nhập điểm RE khi FE dưới 5. Trả True nếu được thi lại, False nếu chưa có FE hoặc FE đã đạt.
    def can_take_re_exam(self, grade_fe: float) -> bool:
        """
        A student takes the re-exam only after failing the final exam,
        so the RE grade is accepted only when FE is below the pass mark.
        """
        # VI: Chưa có điểm FE thì chưa thể thi lại.
        if grade_fe is None:
            return False
        #End if
        # VI: Số 5 là điểm đạt (tương ứng Result.PASS_MARK): chỉ FE rớt mới được thi lại.
        return grade_fe < 5
    #End def
#End class
