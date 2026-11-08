# Result_manager.py
# VI: Lớp manager: file này giữ danh sách kết quả trong bộ nhớ và chạy các luật nghiệp vụ (thêm, sửa, xóa, tìm, GPA, sắp xếp).
# VI: Chứa ResultManagerException và class ResultManager.
# VI: Dùng Result và ResultFileHelper; Main.py gọi ResultManager, không đụng file trực tiếp.
from models.Result import Result
from data_access.Result_file_helper import ResultFileHelper


# VI: Exception riêng báo vi phạm luật nghiệp vụ, ví dụ thêm trùng hoặc sửa kết quả không tồn tại.
class ResultManagerException(Exception):
    """Raised when a result action breaks a business rule."""
    pass
#End class


# VI: Class quản lý toàn bộ kết quả học tập. Dữ liệu là một list vì mỗi sinh viên có nhiều kết quả.
class ResultManager:
    """
    Holds every study result in memory and runs the business rules on them.
    The data lives in a list because one student owns many results.
    """

    # VI: Hàm khởi tạo: tạo file helper và list rỗng.
    def __init__(self):
        self._file_helper = ResultFileHelper()
        self._result_list = []
    #End def

    # VI: Getter của list kết quả. Chỉ đọc, class không có setter.
    @property
    def result_list(self) -> list:
        """Getter for the whole list. Read-only: there is no setter."""
        return self._result_list
    #End def

    # VI: Nạp dữ liệu từ file vào list (thay list cũ). Trả về số kết quả đã đọc.
    def load_data(self) -> int:
        """Reads the data file into the list. Returns how many results were read."""
        self._result_list = self._file_helper.load()
        return len(self._result_list)
    #End def

    # VI: Ghi toàn bộ list ra file qua file helper.
    def save_data(self) -> None:
        """Writes the whole list back to the data file."""
        self._file_helper.save(self._result_list)
    #End def

    # VI: Thêm một Result. Ném ResultManagerException nếu sinh viên đó đã có cùng môn trong cùng học kỳ.
    def add_result(self, result: Result) -> None:
        """
        Adds one result. The same student cannot own two results
        of the same course in the same semester.
        """
        # VI: Khóa của một kết quả là bộ ba (mã sinh viên, mã môn, học kỳ); đã có thì từ chối.
        if self.find_result(result.student_id, result.course_id, result.semester) is not None:
            raise ResultManagerException(
                "Student " + result.student_id + " already has a result of "
                + result.course_id + " in " + result.semester + "."
            )
        #End if
        self._result_list.append(result)
    #End def

    # VI: Tìm kết quả theo bộ ba khóa. Trả về Result hoặc None. Chuẩn hóa chữ (bỏ khoảng trắng, viết hoa) trước khi so.
    def find_result(self, student_id: str, course_id: str, semester: str) -> Result:
        """Returns the one result that matches student, course and semester, or None."""
        student_id = student_id.strip().upper()
        course_id = course_id.strip().upper()
        semester = semester.strip().upper()
        # VI: Duyệt tuần tự, gặp kết quả khớp cả ba trường thì trả về ngay.
        for result in self._result_list:
            if (result.student_id == student_id
                    and result.course_id == course_id
                    and result.semester == semester):
                return result
            #End if
        #End for
        return None
    #End def

    # VI: Sửa hai điểm (FE, RE) của một kết quả. Ném ResultManagerException nếu không tìm thấy.
    # VI: Setter của Result sẽ ném ValueError nếu điểm ngoài khoảng 0 đến 10.
    def update_grade(self, student_id: str, course_id: str, semester: str,
                     grade_fe: float, grade_re: float) -> None:
        """Changes the two grades of one result."""
        result = self.find_result(student_id, course_id, semester)
        if result is None:
            raise ResultManagerException("That result does not exist.")
        #End if
        result.grade_fe = grade_fe
        result.grade_re = grade_re
    #End def

    # VI: Xóa một kết quả và trả về đối tượng vừa xóa. Ném ResultManagerException nếu không tồn tại.
    def delete_result(self, student_id: str, course_id: str, semester: str) -> Result:
        """Removes one result and returns the removed object."""
        result = self.find_result(student_id, course_id, semester)
        if result is None:
            raise ResultManagerException("That result does not exist.")
        #End if
        self._result_list.remove(result)
        return result
    #End def

    # VI: Xóa mọi kết quả của một sinh viên (gọi sau khi xóa sinh viên để không còn dữ liệu mồ côi). Trả về số dòng đã xóa.
    def delete_result_of_student(self, student_id: str) -> int:
        """
        Removes every result of one student. The main program calls this
        after deleting a student so that no orphan result stays behind.
        """
        student_id = student_id.strip().upper()
        # VI: Cách làm: gom các kết quả cần giữ vào keep_list rồi thay list cũ, đếm số kết quả bị loại.
        keep_list = []
        deleted_count = 0
        for result in self._result_list:
            if result.student_id == student_id:
                deleted_count = deleted_count + 1
            else:
                keep_list.append(result)
            #End if
        #End for
        self._result_list = keep_list
        return deleted_count
    #End def

    # VI: Lấy list các kết quả của một sinh viên (list rỗng nếu chưa có).
    def get_result_list_of_student(self, student_id: str) -> list:
        """Returns every result of one student."""
        student_id = student_id.strip().upper()
        result_list = []
        for result in self._result_list:
            if result.student_id == student_id:
                result_list.append(result)
            #End if
        #End for
        return result_list
    #End def

    # VI: Trả về bản sao của list, để bên ngoài sửa list không làm hỏng dữ liệu bên trong.
    def get_all_result_list(self) -> list:
        """Returns every result of every student."""
        return list(self._result_list)
    #End def

    # VI: Tính GPA theo tín chỉ: tổng (điểm tốt nhất x tín chỉ) chia tổng tín chỉ, làm tròn 2 chữ số.
    # VI: Môn chưa có điểm bị bỏ qua. Trả None nếu chưa có môn nào có điểm.
    def calculate_gpa(self, student_id: str) -> float:
        """
        Returns the grade point average of one student, weighted by credits.
        Only results that already hold a grade are counted.
        Returns None when the student has no graded result yet.
        """
        result_list = self.get_result_list_of_student(student_id)
        total_point = 0.0
        total_credits = 0
        for result in result_list:
            best_grade = result.get_best_grade()
            # VI: Môn chưa có điểm (cả FE và RE đều None) thì không tính vào GPA.
            if best_grade is None:
                continue
            #End if
            total_point = total_point + best_grade * result.credits
            total_credits = total_credits + result.credits
        #End for
        # VI: Tránh chia cho 0 khi không có tín chỉ nào được tính.
        if total_credits == 0:
            return None
        #End if
        return round(total_point / total_credits, 2)
    #End def

    # VI: Đếm tổng tín chỉ của các môn đạt (status là Pass, tức điểm tốt nhất từ 5 trở lên). Trả về int.
    def count_passed_credits(self, student_id: str) -> int:
        """Returns how many credits one student has already passed."""
        total_credits = 0
        for result in self.get_result_list_of_student(student_id):
            if result.status == "Pass":
                total_credits = total_credits + result.credits
            #End if
        #End for
        return total_credits
    #End def

    # VI: Sắp xếp kết quả của một sinh viên theo điểm tốt nhất, cao xuống thấp. Trả về list mới.
    def get_sorted_by_grade(self, student_id: str) -> list:
        """Returns the results of one student sorted from the highest grade down."""
        result_list = self.get_result_list_of_student(student_id)
        return sorted(
            result_list,
            # VI: Môn chưa có điểm được tính là -1 để luôn nằm cuối danh sách.
            key=lambda result: result.get_best_grade() if result.get_best_grade() is not None else -1,
            reverse=True
        )
    #End def

    # VI: Sắp xếp mọi kết quả theo trạng thái: Pass, rồi Fail, rồi Not graded. Trả về list mới.
    def get_all_sorted_by_status(self) -> list:
        """
        Returns every result sorted by status, Pass rows first. Menu item 2.4.
        The key turns the status into a number so that Pass sorts before Fail
        and before the rows that have no grade yet.
        """
        # VI: Bảng thứ tự: số nhỏ đứng trước. sorted() giữ nguyên thứ tự cũ giữa các dòng cùng trạng thái.
        order_dict = {"Pass": 0, "Fail": 1, "Not graded": 2}
        return sorted(self._result_list, key=lambda result: order_dict[result.status])
    #End def

    # VI: Lọc các kết quả có trạng thái Pass. Trả về list mới.
    def get_pass_result_list(self) -> list:
        """Returns the results that are Pass. Menu item 2.5."""
        result_list = []
        for result in self._result_list:
            if result.status == "Pass":
                result_list.append(result)
            #End if
        #End for
        return result_list
    #End def

    # VI: Trả về set các mã môn đã xuất hiện; set tự loại mã trùng.
    def get_course_id_set(self) -> set:
        """Returns the set of every course that appears in the data."""
        course_id_set = set()
        for result in self._result_list:
            course_id_set.add(result.course_id)
        #End for
        return course_id_set
    #End def
#End class
