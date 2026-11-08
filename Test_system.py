# Test_system.py
# Automatic tests of the Student Management System.
# Run: python3 Test_system.py
# VI: Đây là file unit test của cả hệ thống, dùng thư viện unittest có sẵn của Python.
# VI: Mỗi class test kiểm một lớp của mô hình: entity, validator, manager, file helper.
# VI: Chạy bằng lệnh: python3 Test_system.py. Các test ghi file chạy trong thư mục _test_data để không ghi đè dữ liệu thật.
import os
import unittest

from Student import Student
from Result import Result
from Student_validator import StudentValidator
from Result_validator import ResultValidator
from Student_manager import StudentManager, StudentManagerException
from Result_manager import ResultManager, ResultManagerException
from Student_file_helper import StudentFileHelper
from Result_file_helper import ResultFileHelper


# VI: Hàm trợ giúp: tạo nhanh một Student mẫu, có thể đổi mã, lớp và trạng thái. Trả về đối tượng Student.
def make_student(student_id: str = "SE00001", class_name: str = "IA2102",
                 status: str = "Active") -> Student:
    """Builds one student for the tests."""
    return Student(student_id, "Nguyen Van A", "15/03/2005", "Male",
                   class_name, "0901234567", "a.nguyen@fpt.edu.vn", status)
#End def


# VI: Nhóm test kiểm entity Student: kế thừa Person, getter, setter, chuẩn hóa chữ.
class TestStudent(unittest.TestCase):
    """Tests the Student entity."""

    # VI: Student kế thừa Person nên đọc được full_name và phone.
    def test_inherits_person(self):
        student = make_student()
        self.assertEqual(student.full_name, "Nguyen Van A")
        self.assertEqual(student.phone, "0901234567")
    #End def

    # VI: student_id chỉ có getter, gán giá trị mới phải ném AttributeError.
    def test_id_is_read_only(self):
        student = make_student()
        with self.assertRaises(AttributeError):
            student.student_id = "SE00002"
        #End with
    #End def

    # VI: Mã sinh viên và lớp nhập chữ thường sẽ được đổi thành chữ hoa.
    def test_id_and_class_are_upper_case(self):
        student = make_student("se00007", "ia2102")
        self.assertEqual(student.student_id, "SE00007")
        self.assertEqual(student.class_name, "IA2102")
    #End def

    # VI: Gán status sai (không thuộc danh sách cho phép) phải ném ValueError.
    def test_status_setter_refuses_a_wrong_value(self):
        student = make_student()
        with self.assertRaises(ValueError):
            student.status = "Sleeping"
        #End with
    #End def

    # VI: is_active chỉ True khi status là Active.
    def test_is_active(self):
        self.assertTrue(make_student(status="Active").is_active())
        self.assertFalse(make_student(status="Graduated").is_active())
    #End def

    # VI: Một Student khi ghi ra file có đúng 8 trường cách nhau bằng |.
    def test_to_file_string_has_eight_fields(self):
        self.assertEqual(len(make_student().to_file_string().split("|")), 8)
    #End def
#End class


# VI: Nhóm test kiểm entity Result: trạng thái Pass, Fail, Not graded và setter điểm.
class TestResult(unittest.TestCase):
    """Tests the Result entity."""

    # VI: FE = 8.5 (từ 5 trở lên) thì status là Pass.
    def test_status_pass_on_the_final_exam(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 8.5, None)
        self.assertEqual(result.status, "Pass")
    #End def

    # VI: FE = 4.0 trượt nhưng RE = 6.5 đạt nên status là Pass.
    def test_status_pass_on_the_re_exam(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 4.0, 6.5)
        self.assertEqual(result.status, "Pass")
    #End def

    # VI: Cả FE và RE đều dưới 5 thì status là Fail.
    def test_status_fail(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 3.0, 4.0)
        self.assertEqual(result.status, "Fail")
    #End def

    # VI: Chưa có điểm nào thì status là Not graded.
    def test_status_not_graded(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, None, None)
        self.assertEqual(result.status, "Not graded")
    #End def

    # VI: status chỉ có getter, gán giá trị mới phải ném AttributeError.
    def test_status_is_read_only(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 8.0, None)
        with self.assertRaises(AttributeError):
            result.status = "Pass"
        #End with
    #End def

    # VI: Có cả FE và RE thì điểm tốt nhất là RE = 6.5.
    def test_get_best_grade(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 4.0, 6.5)
        self.assertEqual(result.get_best_grade(), 6.5)
    #End def

    # VI: Gán điểm lớn hơn 10 phải ném ValueError.
    def test_grade_setter_refuses_a_grade_over_ten(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 8.0, None)
        with self.assertRaises(ValueError):
            result.grade_fe = 11
        #End with
    #End def
#End class


# VI: Nhóm test kiểm StudentValidator: mã sinh viên, ngày sinh, số điện thoại, email, trạng thái, giới tính.
class TestStudentValidator(unittest.TestCase):
    """Tests every check of the student validator."""

    # VI: setUp chạy trước mỗi test, tạo validator mới.
    def setUp(self):
        self._validator = StudentValidator()
    #End def

    # VI: Mã sinh viên: SE + số hợp lệ thì đúng, sai tiền tố hoặc thiếu số thì sai.
    def test_student_id(self):
        self.assertTrue(self._validator.is_valid_student_id("SE00001"))
        self.assertTrue(self._validator.is_valid_student_id("SE123456"))
        self.assertFalse(self._validator.is_valid_student_id("AB00001"))
        self.assertFalse(self._validator.is_valid_student_id("SE001"))
    #End def

    # VI: Ngày sinh: kiểm năm nhuận (29/02/2004 đúng, 2005 sai), ngày không có trong tháng và sai dạng dd/mm/yyyy.
    def test_date_of_birth(self):
        self.assertTrue(self._validator.is_valid_date_of_birth("29/02/2004"))
        self.assertFalse(self._validator.is_valid_date_of_birth("29/02/2005"))
        self.assertFalse(self._validator.is_valid_date_of_birth("31/04/2005"))
        self.assertFalse(self._validator.is_valid_date_of_birth("1/1/2005"))
    #End def

    # VI: Số điện thoại phải đủ 10 số bắt đầu bằng 0: thiếu hoặc thừa số đều sai.
    def test_phone(self):
        self.assertTrue(self._validator.is_valid_phone("0901234567"))
        self.assertFalse(self._validator.is_valid_phone("901234567"))
        self.assertFalse(self._validator.is_valid_phone("09012345678"))
    #End def

    # VI: Email phải có @ và tên miền có dấu chấm.
    def test_email(self):
        self.assertTrue(self._validator.is_valid_email("a.nguyen@fpt.edu.vn"))
        self.assertFalse(self._validator.is_valid_email("a.nguyen@fpt"))
        self.assertFalse(self._validator.is_valid_email("a.nguyen.fpt.edu.vn"))
    #End def

    # VI: Trạng thái và giới tính không phân biệt hoa thường, giá trị lạ thì sai.
    def test_status_and_gender(self):
        self.assertTrue(self._validator.is_valid_status("active"))
        self.assertFalse(self._validator.is_valid_status("Studying"))
        self.assertTrue(self._validator.is_valid_gender("female"))
        self.assertFalse(self._validator.is_valid_gender("Other"))
    #End def
#End class


# VI: Nhóm test kiểm ResultValidator: học kỳ, tín chỉ, điểm, quyền thi lại.
class TestResultValidator(unittest.TestCase):
    """Tests every check of the result validator."""

    # VI: setUp chạy trước mỗi test, tạo validator mới.
    def setUp(self):
        self._validator = ResultValidator()
    #End def

    # VI: Học kỳ đúng dạng FA26 thì hợp lệ, FALL26 thì sai.
    def test_semester(self):
        self.assertTrue(self._validator.is_valid_semester("FA26"))
        self.assertFalse(self._validator.is_valid_semester("FALL26"))
    #End def

    # VI: Tín chỉ chỉ hợp lệ từ 1 đến 4, nên 0 và 5 đều sai.
    def test_credits(self):
        self.assertTrue(self._validator.is_valid_credits(3))
        self.assertFalse(self._validator.is_valid_credits(0))
        self.assertFalse(self._validator.is_valid_credits(5))
    #End def

    # VI: Điểm hợp lệ từ 0 đến 10 và cho phép None (chưa thi); 10.5 thì sai.
    def test_grade(self):
        self.assertTrue(self._validator.is_valid_grade(0))
        self.assertTrue(self._validator.is_valid_grade(10))
        self.assertTrue(self._validator.is_valid_grade(None))
        self.assertFalse(self._validator.is_valid_grade(10.5))
    #End def

    # VI: Chỉ được thi lại khi FE dưới 5: FE = 3.0 được, FE = 7.0 hoặc chưa thi thì không.
    def test_can_take_re_exam(self):
        self.assertTrue(self._validator.can_take_re_exam(3.0))
        self.assertFalse(self._validator.can_take_re_exam(7.0))
        self.assertFalse(self._validator.can_take_re_exam(None))
    #End def
#End class


# VI: Nhóm test kiểm StudentManager: thêm, tìm, sửa, xóa, tìm kiếm, sắp xếp, thống kê.
class TestStudentManager(unittest.TestCase):
    """Tests the business rules on students."""

    # VI: setUp chạy trước mỗi test, tạo manager mới với list rỗng.
    def setUp(self):
        self._manager = StudentManager()
    #End def

    # VI: Thêm một sinh viên rồi tìm bằng mã viết thường vẫn thấy.
    def test_add_and_find(self):
        self._manager.add_student(make_student("SE00001"))
        self.assertIsNotNone(self._manager.find_student_by_id("se00001"))
    #End def

    # VI: Thêm hai sinh viên cùng mã phải ném StudentManagerException.
    def test_add_refuses_a_duplicated_id(self):
        self._manager.add_student(make_student("SE00001"))
        with self.assertRaises(StudentManagerException):
            self._manager.add_student(make_student("SE00001"))
        #End with
    #End def

    # VI: Sửa sinh viên không tồn tại phải ném StudentManagerException.
    def test_update_a_missing_student(self):
        with self.assertRaises(StudentManagerException):
            self._manager.update_student("SE09999", "phone", "0909090909")
        #End with
    #End def

    # VI: Sau khi xóa, tìm lại mã đó phải trả None.
    def test_delete(self):
        self._manager.add_student(make_student("SE00001"))
        self._manager.delete_student("SE00001")
        self.assertIsNone(self._manager.find_student_by_id("SE00001"))
    #End def

    # VI: Tìm theo tên (một phần, không phân biệt hoa thường) ra 2 người; tìm theo lớp ra 1 người.
    def test_search_by_name_and_class(self):
        self._manager.add_student(make_student("SE00001", "IA2102"))
        self._manager.add_student(make_student("SE00002", "IA2103"))
        self.assertEqual(len(self._manager.search_by_name("van a")), 2)
        self.assertEqual(len(self._manager.search_by_class("ia2103")), 1)
    #End def

    # VI: Thêm mã SE00003 trước SE00001, sắp xếp theo mã phải đưa SE00001 lên đầu.
    def test_sorted_by_id(self):
        self._manager.add_student(make_student("SE00003"))
        self._manager.add_student(make_student("SE00001"))
        id_list = [student.student_id for student in self._manager.get_sorted_by_id()]
        self.assertEqual(id_list, ["SE00001", "SE00003"])
    #End def

    # VI: Đếm theo trạng thái: có 1 Active, 0 Inactive.
    def test_count_by_status(self):
        self._manager.add_student(make_student("SE00001", status="Active"))
        self._manager.add_student(make_student("SE00002", status="Graduated"))
        count_dict = self._manager.count_by_status()
        self.assertEqual(count_dict["Active"], 1)
        self.assertEqual(count_dict["Inactive"], 0)
    #End def

    # VI: Tìm theo trạng thái graduated (chữ thường) ra đúng 1 sinh viên.
    def test_search_by_status(self):
        self._manager.add_student(make_student("SE00001", status="Active"))
        self._manager.add_student(make_student("SE00002", status="Graduated"))
        self.assertEqual(len(self._manager.search_by_status("graduated")), 1)
    #End def

    # VI: Danh sách sinh viên đang học chỉ gồm người có trạng thái Active.
    def test_active_student_list(self):
        self._manager.add_student(make_student("SE00001", status="Active"))
        self._manager.add_student(make_student("SE00002", status="Inactive"))
        self.assertEqual(len(self._manager.get_active_student_list()), 1)
    #End def

    # VI: Hai sinh viên cùng lớp thì tập hợp tên lớp chỉ có một phần tử (set loại trùng).
    def test_class_name_set(self):
        self._manager.add_student(make_student("SE00001", "IA2102"))
        self._manager.add_student(make_student("SE00002", "IA2102"))
        self.assertEqual(self._manager.get_class_name_set(), {"IA2102"})
    #End def
#End class


# VI: Nhóm test kiểm ResultManager: thêm trùng, GPA, tín chỉ đạt, xóa, sắp xếp, lọc Pass.
class TestResultManager(unittest.TestCase):
    """Tests the business rules on study results."""

    # VI: setUp chạy trước mỗi test: SE00001 có 2 môn, PFP191 (FE 8.0) và MAE101 (FE 4.0, RE 6.0), mỗi môn 3 tín chỉ.
    def setUp(self):
        self._manager = ResultManager()
        self._manager.add_result(Result("SE00001", "PFP191", "Python", "FA26", 3, 8.0, None))
        self._manager.add_result(Result("SE00001", "MAE101", "Maths", "FA26", 3, 4.0, 6.0))
    #End def

    # VI: Thêm cùng sinh viên, môn và học kỳ lần nữa phải ném ResultManagerException.
    def test_add_refuses_the_same_course_twice(self):
        with self.assertRaises(ResultManagerException):
            self._manager.add_result(Result("SE00001", "PFP191", "Python", "FA26", 3, 5.0, None))
        #End with
    #End def

    # VI: GPA = (8.0 x 3 + 6.0 x 3) / 6 = 7.0, môn MAE101 lấy điểm RE.
    def test_gpa(self):
        # (8.0 * 3 + 6.0 * 3) / 6 = 7.0
        self.assertEqual(self._manager.calculate_gpa("SE00001"), 7.0)
    #End def

    # VI: Sinh viên chỉ có môn chưa có điểm thì GPA là None.
    def test_gpa_without_a_grade(self):
        self._manager.add_result(Result("SE00002", "PFP191", "Python", "FA26", 3, None, None))
        self.assertIsNone(self._manager.calculate_gpa("SE00002"))
    #End def

    # VI: Cả hai môn đều đạt nên số tín chỉ đạt là 3 + 3 = 6.
    def test_passed_credits(self):
        self.assertEqual(self._manager.count_passed_credits("SE00001"), 6)
    #End def

    # VI: Xóa mọi kết quả của SE00001 trả về 2 và list còn lại rỗng.
    def test_delete_every_result_of_one_student(self):
        deleted_count = self._manager.delete_result_of_student("SE00001")
        self.assertEqual(deleted_count, 2)
        self.assertEqual(len(self._manager.get_all_result_list()), 0)
    #End def

    # VI: Xóa kết quả không tồn tại phải ném ResultManagerException.
    def test_delete_a_missing_result(self):
        with self.assertRaises(ResultManagerException):
            self._manager.delete_result("SE00009", "PFP191", "FA26")
        #End with
    #End def

    # VI: Sắp xếp theo trạng thái: Pass đứng đầu, Not graded đứng cuối.
    def test_sorted_by_status_puts_pass_first(self):
        self._manager.add_result(Result("SE00002", "CSI104", "CS", "FA26", 3, 2.0, 3.0))
        self._manager.add_result(Result("SE00003", "CSI104", "CS", "FA26", 3, None, None))
        status_list = [result.status for result in self._manager.get_all_sorted_by_status()]
        self.assertEqual(status_list[0], "Pass")
        self.assertEqual(status_list[-1], "Not graded")
    #End def

    # VI: Thêm một kết quả Fail (2.0 và 3.0) thì vẫn chỉ có 2 kết quả Pass.
    def test_pass_result_list(self):
        self._manager.add_result(Result("SE00002", "CSI104", "CS", "FA26", 3, 2.0, 3.0))
        self.assertEqual(len(self._manager.get_pass_result_list()), 2)
    #End def

    # VI: Sắp xếp theo điểm giảm dần: PFP191 (8.0) đứng trước MAE101 (6.0).
    def test_sorted_by_grade(self):
        result_list = self._manager.get_sorted_by_grade("SE00001")
        self.assertEqual(result_list[0].course_id, "PFP191")
    #End def
#End class


# VI: Nhóm test kiểm file helper: lưu rồi đọc lại phải ra đúng dữ liệu (round trip).
class TestFileHelper(unittest.TestCase):
    """Tests that saving then loading gives the same data back."""

    # VI: Lưu 2 sinh viên rồi nạp lại: đủ 2 người và dòng đầu giống hệt bản gốc.
    def test_student_file_round_trip(self):
        helper = StudentFileHelper()
        student_list = [make_student("SE00001"), make_student("SE00002")]
        helper.save(student_list)
        loaded_list = helper.load()
        self.assertEqual(len(loaded_list), 2)
        self.assertEqual(loaded_list[0].to_file_string(), student_list[0].to_file_string())
    #End def

    # VI: Lưu kết quả chưa có điểm rồi nạp lại: điểm vẫn là None và status vẫn là Not graded.
    def test_result_file_round_trip_keeps_an_empty_grade(self):
        helper = ResultFileHelper()
        result_list = [Result("SE00001", "PFP191", "Python", "FA26", 3, None, None)]
        helper.save(result_list)
        loaded_list = helper.load()
        self.assertEqual(len(loaded_list), 1)
        self.assertIsNone(loaded_list[0].grade_fe)
        self.assertEqual(loaded_list[0].status, "Not graded")
    #End def
#End class


# VI: Nhóm test kiểm file bị hỏng: dòng lỗi phải bị bỏ qua, chương trình không được dừng.
class TestBrokenFile(unittest.TestCase):
    """Tests that a broken line is skipped instead of stopping the program."""

    # VI: Một dòng có status sai (Sleeping) bị bỏ, chỉ nạp được dòng hợp lệ (1 sinh viên).
    def test_a_wrong_status_does_not_stop_the_load(self):
        with open("students_data.txt", "w", encoding="utf-8") as file_out:
            file_out.write(make_student("SE00001").to_file_string() + "\n")
            file_out.write("SE00002|B|01/01/2005|Male|IA2102|0901234567|b@fpt.edu.vn|Sleeping\n")
        #End with
        self.assertEqual(len(StudentFileHelper().load()), 1)
    #End def

    # VI: Dòng sai số trường bị bỏ qua nên kết quả là list rỗng.
    def test_a_wrong_field_count_is_skipped(self):
        with open("students_data.txt", "w", encoding="utf-8") as file_out:
            file_out.write("SE00001|only|three|fields\n")
        #End with
        self.assertEqual(len(StudentFileHelper().load()), 0)
    #End def

    # VI: Dòng có điểm 12.0 bị bỏ, dòng điểm 8.0 vẫn được nạp (còn 1 kết quả).
    def test_a_grade_over_ten_is_skipped(self):
        with open("results_data.txt", "w", encoding="utf-8") as file_out:
            file_out.write("SE00001|PFP191|Python|FA26|3|12.0|\n")
            file_out.write("SE00001|MAE101|Maths|FA26|3|8.0|\n")
        #End with
        self.assertEqual(len(ResultFileHelper().load()), 1)
    #End def

    # VI: Xóa file rồi nạp: chưa có file thì chương trình bắt đầu với list rỗng.
    def test_a_missing_file_starts_an_empty_program(self):
        if os.path.exists("students_data.txt"):
            os.remove("students_data.txt")
        #End if
        self.assertEqual(StudentFileHelper().load(), [])
    #End def
#End class


if __name__ == "__main__":
    # VI: Khối này chạy khi gọi trực tiếp file. Chuyển vào thư mục _test_data trước để test không ghi đè dữ liệu thật.
    # The file tests overwrite the data files, so they run in a temporary folder.
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_test_data"))
    unittest.main(verbosity=2)
#End if
