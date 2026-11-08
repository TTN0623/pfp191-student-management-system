# Test_system.py
# Automatic tests of the Student Management System.
# Run: python3 Test_system.py
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


def make_student(student_id: str = "SE00001", class_name: str = "IA2102",
                 status: str = "Active") -> Student:
    """Builds one student for the tests."""
    return Student(student_id, "Nguyen Van A", "15/03/2005", "Male",
                   class_name, "0901234567", "a.nguyen@fpt.edu.vn", status)
#End def


class TestStudent(unittest.TestCase):
    """Tests the Student entity."""

    def test_inherits_person(self):
        student = make_student()
        self.assertEqual(student.full_name, "Nguyen Van A")
        self.assertEqual(student.phone, "0901234567")
    #End def

    def test_id_is_read_only(self):
        student = make_student()
        with self.assertRaises(AttributeError):
            student.student_id = "SE00002"
        #End with
    #End def

    def test_id_and_class_are_upper_case(self):
        student = make_student("se00007", "ia2102")
        self.assertEqual(student.student_id, "SE00007")
        self.assertEqual(student.class_name, "IA2102")
    #End def

    def test_status_setter_refuses_a_wrong_value(self):
        student = make_student()
        with self.assertRaises(ValueError):
            student.status = "Sleeping"
        #End with
    #End def

    def test_is_active(self):
        self.assertTrue(make_student(status="Active").is_active())
        self.assertFalse(make_student(status="Graduated").is_active())
    #End def

    def test_to_file_string_has_eight_fields(self):
        self.assertEqual(len(make_student().to_file_string().split("|")), 8)
    #End def
#End class


class TestResult(unittest.TestCase):
    """Tests the Result entity."""

    def test_status_pass_on_the_final_exam(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 8.5, None)
        self.assertEqual(result.status, "Pass")
    #End def

    def test_status_pass_on_the_re_exam(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 4.0, 6.5)
        self.assertEqual(result.status, "Pass")
    #End def

    def test_status_fail(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 3.0, 4.0)
        self.assertEqual(result.status, "Fail")
    #End def

    def test_status_not_graded(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, None, None)
        self.assertEqual(result.status, "Not graded")
    #End def

    def test_status_is_read_only(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 8.0, None)
        with self.assertRaises(AttributeError):
            result.status = "Pass"
        #End with
    #End def

    def test_get_best_grade(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 4.0, 6.5)
        self.assertEqual(result.get_best_grade(), 6.5)
    #End def

    def test_grade_setter_refuses_a_grade_over_ten(self):
        result = Result("SE00001", "PFP191", "Python", "FA26", 3, 8.0, None)
        with self.assertRaises(ValueError):
            result.grade_fe = 11
        #End with
    #End def
#End class


class TestStudentValidator(unittest.TestCase):
    """Tests every check of the student validator."""

    def setUp(self):
        self._validator = StudentValidator()
    #End def

    def test_student_id(self):
        self.assertTrue(self._validator.is_valid_student_id("SE00001"))
        self.assertTrue(self._validator.is_valid_student_id("SE123456"))
        self.assertFalse(self._validator.is_valid_student_id("AB00001"))
        self.assertFalse(self._validator.is_valid_student_id("SE001"))
    #End def

    def test_date_of_birth(self):
        self.assertTrue(self._validator.is_valid_date_of_birth("29/02/2004"))
        self.assertFalse(self._validator.is_valid_date_of_birth("29/02/2005"))
        self.assertFalse(self._validator.is_valid_date_of_birth("31/04/2005"))
        self.assertFalse(self._validator.is_valid_date_of_birth("1/1/2005"))
    #End def

    def test_phone(self):
        self.assertTrue(self._validator.is_valid_phone("0901234567"))
        self.assertFalse(self._validator.is_valid_phone("901234567"))
        self.assertFalse(self._validator.is_valid_phone("09012345678"))
    #End def

    def test_email(self):
        self.assertTrue(self._validator.is_valid_email("a.nguyen@fpt.edu.vn"))
        self.assertFalse(self._validator.is_valid_email("a.nguyen@fpt"))
        self.assertFalse(self._validator.is_valid_email("a.nguyen.fpt.edu.vn"))
    #End def

    def test_status_and_gender(self):
        self.assertTrue(self._validator.is_valid_status("active"))
        self.assertFalse(self._validator.is_valid_status("Studying"))
        self.assertTrue(self._validator.is_valid_gender("female"))
        self.assertFalse(self._validator.is_valid_gender("Other"))
    #End def
#End class


class TestResultValidator(unittest.TestCase):
    """Tests every check of the result validator."""

    def setUp(self):
        self._validator = ResultValidator()
    #End def

    def test_semester(self):
        self.assertTrue(self._validator.is_valid_semester("FA26"))
        self.assertFalse(self._validator.is_valid_semester("FALL26"))
    #End def

    def test_credits(self):
        self.assertTrue(self._validator.is_valid_credits(3))
        self.assertFalse(self._validator.is_valid_credits(0))
        self.assertFalse(self._validator.is_valid_credits(5))
    #End def

    def test_grade(self):
        self.assertTrue(self._validator.is_valid_grade(0))
        self.assertTrue(self._validator.is_valid_grade(10))
        self.assertTrue(self._validator.is_valid_grade(None))
        self.assertFalse(self._validator.is_valid_grade(10.5))
    #End def

    def test_can_take_re_exam(self):
        self.assertTrue(self._validator.can_take_re_exam(3.0))
        self.assertFalse(self._validator.can_take_re_exam(7.0))
        self.assertFalse(self._validator.can_take_re_exam(None))
    #End def
#End class


class TestStudentManager(unittest.TestCase):
    """Tests the business rules on students."""

    def setUp(self):
        self._manager = StudentManager()
    #End def

    def test_add_and_find(self):
        self._manager.add_student(make_student("SE00001"))
        self.assertIsNotNone(self._manager.find_student_by_id("se00001"))
    #End def

    def test_add_refuses_a_duplicated_id(self):
        self._manager.add_student(make_student("SE00001"))
        with self.assertRaises(StudentManagerException):
            self._manager.add_student(make_student("SE00001"))
        #End with
    #End def

    def test_update_a_missing_student(self):
        with self.assertRaises(StudentManagerException):
            self._manager.update_student("SE09999", "phone", "0909090909")
        #End with
    #End def

    def test_delete(self):
        self._manager.add_student(make_student("SE00001"))
        self._manager.delete_student("SE00001")
        self.assertIsNone(self._manager.find_student_by_id("SE00001"))
    #End def

    def test_search_by_name_and_class(self):
        self._manager.add_student(make_student("SE00001", "IA2102"))
        self._manager.add_student(make_student("SE00002", "IA2103"))
        self.assertEqual(len(self._manager.search_by_name("van a")), 2)
        self.assertEqual(len(self._manager.search_by_class("ia2103")), 1)
    #End def

    def test_sorted_by_id(self):
        self._manager.add_student(make_student("SE00003"))
        self._manager.add_student(make_student("SE00001"))
        id_list = [student.student_id for student in self._manager.get_sorted_by_id()]
        self.assertEqual(id_list, ["SE00001", "SE00003"])
    #End def

    def test_count_by_status(self):
        self._manager.add_student(make_student("SE00001", status="Active"))
        self._manager.add_student(make_student("SE00002", status="Graduated"))
        count_dict = self._manager.count_by_status()
        self.assertEqual(count_dict["Active"], 1)
        self.assertEqual(count_dict["Inactive"], 0)
    #End def

    def test_search_by_status(self):
        self._manager.add_student(make_student("SE00001", status="Active"))
        self._manager.add_student(make_student("SE00002", status="Graduated"))
        self.assertEqual(len(self._manager.search_by_status("graduated")), 1)
    #End def

    def test_active_student_list(self):
        self._manager.add_student(make_student("SE00001", status="Active"))
        self._manager.add_student(make_student("SE00002", status="Inactive"))
        self.assertEqual(len(self._manager.get_active_student_list()), 1)
    #End def

    def test_class_name_set(self):
        self._manager.add_student(make_student("SE00001", "IA2102"))
        self._manager.add_student(make_student("SE00002", "IA2102"))
        self.assertEqual(self._manager.get_class_name_set(), {"IA2102"})
    #End def
#End class


class TestResultManager(unittest.TestCase):
    """Tests the business rules on study results."""

    def setUp(self):
        self._manager = ResultManager()
        self._manager.add_result(Result("SE00001", "PFP191", "Python", "FA26", 3, 8.0, None))
        self._manager.add_result(Result("SE00001", "MAE101", "Maths", "FA26", 3, 4.0, 6.0))
    #End def

    def test_add_refuses_the_same_course_twice(self):
        with self.assertRaises(ResultManagerException):
            self._manager.add_result(Result("SE00001", "PFP191", "Python", "FA26", 3, 5.0, None))
        #End with
    #End def

    def test_gpa(self):
        # (8.0 * 3 + 6.0 * 3) / 6 = 7.0
        self.assertEqual(self._manager.calculate_gpa("SE00001"), 7.0)
    #End def

    def test_gpa_without_a_grade(self):
        self._manager.add_result(Result("SE00002", "PFP191", "Python", "FA26", 3, None, None))
        self.assertIsNone(self._manager.calculate_gpa("SE00002"))
    #End def

    def test_passed_credits(self):
        self.assertEqual(self._manager.count_passed_credits("SE00001"), 6)
    #End def

    def test_delete_every_result_of_one_student(self):
        deleted_count = self._manager.delete_result_of_student("SE00001")
        self.assertEqual(deleted_count, 2)
        self.assertEqual(len(self._manager.get_all_result_list()), 0)
    #End def

    def test_delete_a_missing_result(self):
        with self.assertRaises(ResultManagerException):
            self._manager.delete_result("SE00009", "PFP191", "FA26")
        #End with
    #End def

    def test_sorted_by_status_puts_pass_first(self):
        self._manager.add_result(Result("SE00002", "CSI104", "CS", "FA26", 3, 2.0, 3.0))
        self._manager.add_result(Result("SE00003", "CSI104", "CS", "FA26", 3, None, None))
        status_list = [result.status for result in self._manager.get_all_sorted_by_status()]
        self.assertEqual(status_list[0], "Pass")
        self.assertEqual(status_list[-1], "Not graded")
    #End def

    def test_pass_result_list(self):
        self._manager.add_result(Result("SE00002", "CSI104", "CS", "FA26", 3, 2.0, 3.0))
        self.assertEqual(len(self._manager.get_pass_result_list()), 2)
    #End def

    def test_sorted_by_grade(self):
        result_list = self._manager.get_sorted_by_grade("SE00001")
        self.assertEqual(result_list[0].course_id, "PFP191")
    #End def
#End class


class TestFileHelper(unittest.TestCase):
    """Tests that saving then loading gives the same data back."""

    def test_student_file_round_trip(self):
        helper = StudentFileHelper()
        student_list = [make_student("SE00001"), make_student("SE00002")]
        helper.save(student_list)
        loaded_list = helper.load()
        self.assertEqual(len(loaded_list), 2)
        self.assertEqual(loaded_list[0].to_file_string(), student_list[0].to_file_string())
    #End def

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


class TestBrokenFile(unittest.TestCase):
    """Tests that a broken line is skipped instead of stopping the program."""

    def test_a_wrong_status_does_not_stop_the_load(self):
        with open("students_data.txt", "w", encoding="utf-8") as file_out:
            file_out.write(make_student("SE00001").to_file_string() + "\n")
            file_out.write("SE00002|B|01/01/2005|Male|IA2102|0901234567|b@fpt.edu.vn|Sleeping\n")
        #End with
        self.assertEqual(len(StudentFileHelper().load()), 1)
    #End def

    def test_a_wrong_field_count_is_skipped(self):
        with open("students_data.txt", "w", encoding="utf-8") as file_out:
            file_out.write("SE00001|only|three|fields\n")
        #End with
        self.assertEqual(len(StudentFileHelper().load()), 0)
    #End def

    def test_a_grade_over_ten_is_skipped(self):
        with open("results_data.txt", "w", encoding="utf-8") as file_out:
            file_out.write("SE00001|PFP191|Python|FA26|3|12.0|\n")
            file_out.write("SE00001|MAE101|Maths|FA26|3|8.0|\n")
        #End with
        self.assertEqual(len(ResultFileHelper().load()), 1)
    #End def

    def test_a_missing_file_starts_an_empty_program(self):
        if os.path.exists("students_data.txt"):
            os.remove("students_data.txt")
        #End if
        self.assertEqual(StudentFileHelper().load(), [])
    #End def
#End class


if __name__ == "__main__":
    # The file tests overwrite the data files, so they run in a temporary folder.
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_test_data"))
    unittest.main(verbosity=2)
#End if
