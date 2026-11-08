# Main.py
# VI: Thuộc lớp điều phối (menu): file chạy chính, bắt đầu chương trình từ đây bằng python Main.py.
# VI: Gọi Student_manager, Student_io, Student_file_helper và các file Result_* tương ứng.
# VI: Chỉ nối các lớp lại với nhau, không chứa luật nghiệp vụ.
# Student Management System - Group 01 - IA2102 - PFP191
# This file only runs the menus. Every rule lives in the manager classes,
# every print lives in the console IO classes, every file access lives in
# the file helper classes.

from services.Student_manager import StudentManager, StudentManagerException
from presentation.Student_io import StudentConsoleIO
from data_access.Student_file_helper import FileIOException as StudentFileIOException
from services.Result_manager import ResultManager, ResultManagerException
from presentation.Result_io import ResultConsoleIO
from data_access.Result_file_helper import FileIOException as ResultFileIOException


# VI: In menu chính (quản lý sinh viên, quản lý kết quả, lưu, thoát).
def show_main_menu() -> None:
    """Prints the main menu of the program."""
    print("\n" + "=" * 46)
    print("     STUDENT MANAGEMENT SYSTEM - GROUP 01")
    print("=" * 46)
    print("1. Manage students")
    print("2. Manage study results")
    print("3. Save every change to file")
    print("0. Save and exit")
#End def


# VI: Tạo dict {mã SV: họ tên} để bảng kết quả hiển thị được tên sinh viên.
def build_name_dict(student_manager: StudentManager) -> dict:
    """Maps every student ID to the full name, so result tables can show the name."""
    name_dict = {}
    for student in student_manager.get_all_student_list():
        name_dict[student.student_id] = student.full_name
    #End for
    return name_dict
#End def


# VI: Vòng lặp menu sinh viên. Chọn 0 để thoát hàm và quay về menu chính.
# VI: Lỗi nghiệp vụ (StudentManagerException) và lỗi giá trị (ValueError) được bắt ở cuối để chương trình không sập.
def run_student_menu(student_manager: StudentManager, student_io: StudentConsoleIO,
                     result_manager: ResultManager) -> None:
    """Runs the student menu until the user goes back."""
    while True:
        student_io.show_student_menu()
        # VI: Đọc lựa chọn menu, chỉ nhận số từ 0 đến 8.
        choice = student_io.read_menu_choice(0, 8)

        if choice == 0:
            return
        #End if

        try:
            if choice == 1:
                # VI: Thêm sinh viên: đọc dữ liệu đã kiểm tra, manager sẽ ném lỗi nếu mã SV bị trùng.
                # 1.1 Add a new student
                student = student_io.read_new_student()
                student_manager.add_student(student)
                student_io.show_message("Added student " + student.student_id + ".")

            elif choice == 2:
                # VI: Cập nhật: phải kiểm tra mã SV có tồn tại trước, rồi mới hỏi trường cần sửa và giá trị mới.
                # 1.2 Update student information
                student_id = student_io.read_student_id("ID of the student to update: ")
                if student_manager.find_student_by_id(student_id) is None:
                    student_io.show_message("No student has that ID.")
                else:
                    field_name = student_io.read_field_to_update()
                    new_value = student_io.read_new_value(field_name)
                    student_manager.update_student(student_id, field_name, new_value)
                    student_io.show_message("Updated " + field_name + ".")
                #End if

            elif choice == 3:
                # VI: Lọc: chọn 1 thì lọc theo lớp, ngược lại lọc theo trạng thái.
                # 1.3 Filter students by class or status
                if student_io.read_filter_choice() == 1:
                    class_name = student_io.read_class_name()
                    student_io.display_student_list(student_manager.search_by_class(class_name))
                else:
                    status = student_io.read_status()
                    student_io.display_student_list(student_manager.search_by_status(status))
                #End if

            elif choice == 4:
                # 1.4 Display active students
                student_io.display_student_list(student_manager.get_active_student_list())

            elif choice == 5:
                # VI: Chọn 5: hiển thị toàn bộ sinh viên, sắp xếp theo mã SV.
                student_io.display_student_list(student_manager.get_sorted_by_id())

            elif choice == 6:
                # VI: Chọn 6: tìm sinh viên có tên chứa từ khóa.
                keyword = student_io.read_text("Part of the name to search: ")
                student_io.display_student_list(student_manager.search_by_name(keyword))

            elif choice == 7:
                student_id = student_io.read_student_id("ID of the student to delete: ")
                # VI: Chọn 7: xóa sinh viên, đồng thời xóa luôn kết quả học của sinh viên đó để dữ liệu không bị mồ côi.
                student = student_manager.delete_student(student_id)
                deleted_count = result_manager.delete_result_of_student(student_id)
                student_io.show_message(
                    "Deleted " + student.full_name + " and " + str(deleted_count) + " result(s)."
                )

            elif choice == 8:
                # VI: Chọn 8: thống kê số sinh viên theo từng trạng thái.
                student_io.display_count_by_status(student_manager.count_by_status())
            #End if

        # VI: Lỗi do manager ném (vd mã SV trùng, không tìm thấy): hiện thông báo rồi quay lại menu.
        except StudentManagerException as error:
            student_io.show_message("Error: " + str(error))
        except ValueError as error:
            student_io.show_message("Wrong value: " + str(error))
        #End try
    #End while
#End def


# VI: Vòng lặp menu kết quả học tập. Chọn 0 để quay về menu chính. Cách bắt lỗi giống menu sinh viên.
def run_result_menu(result_manager: ResultManager, result_io: ResultConsoleIO,
                    student_manager: StudentManager, student_io: StudentConsoleIO) -> None:
    """Runs the result menu until the user goes back."""
    while True:
        result_io.show_result_menu()
        # VI: Đọc lựa chọn menu, chỉ nhận số từ 0 đến 7.
        choice = result_io.read_menu_choice(0, 7)

        if choice == 0:
            return
        #End if

        try:
            if choice == 1:
                # VI: Thêm điểm: sinh viên phải tồn tại trước. Trạng thái Pass/Fail do class Result tự tính từ điểm.
                # 2.1 Add a course grade
                student_id = student_io.read_student_id("ID of the student: ")
                if student_manager.find_student_by_id(student_id) is None:
                    result_io.show_message("No student has that ID. Add the student first.")
                else:
                    result = result_io.read_new_result(student_id)
                    result_manager.add_result(result)
                    result_io.show_message(
                        "Added the result of " + result.course_id + ", status " + result.status + "."
                    )
                #End if

            elif choice == 2:
                # VI: Sửa điểm FE và RE của một môn trong một kỳ, rồi lấy lại kết quả để hiển thị trạng thái mới.
                # 2.2 Update a grade
                student_id = student_io.read_student_id("ID of the student: ")
                course_id = result_io.read_course_id()
                semester = result_io.read_semester()
                # VI: Chỉ hỏi điểm RE khi điểm FE dưới 5 (việc này do read_grade_pair xử lý).
                grade_fe, grade_re = result_io.read_grade_pair()
                result_manager.update_grade(student_id, course_id, semester, grade_fe, grade_re)
                result = result_manager.find_result(student_id, course_id, semester)
                result_io.show_message("Updated the grades, status is now " + result.status + ".")

            elif choice == 3:
                # VI: Xem kết quả của một sinh viên, sắp theo điểm.
                # 2.3 Search enrollments by student ID
                student_id = student_io.read_student_id("ID of the student: ")
                result_io.display_result_list(
                    result_manager.get_sorted_by_grade(student_id), build_name_dict(student_manager)
                )

            elif choice == 4:
                # VI: Xem toàn bộ kết quả, sắp theo trạng thái.
                # 2.4 Display results sorted by status
                result_io.display_result_list(
                    result_manager.get_all_sorted_by_status(), build_name_dict(student_manager)
                )

            elif choice == 5:
                # VI: Chỉ hiển thị các kết quả đạt (Pass).
                # 2.5 Display students with Pass
                result_io.display_result_list(
                    result_manager.get_pass_result_list(), build_name_dict(student_manager)
                )

            elif choice == 6:
                # VI: Tính GPA: kiểm tra sinh viên tồn tại, rồi hiển thị GPA và số tín chỉ đã đạt.
                # 2.6 Calculate the GPA
                student_id = student_io.read_student_id("ID of the student: ")
                student = student_manager.find_student_by_id(student_id)
                if student is None:
                    result_io.show_message("No student has that ID.")
                else:
                    result_io.display_gpa(
                        student_id,
                        student.full_name,
                        result_manager.calculate_gpa(student_id),
                        result_manager.count_passed_credits(student_id)
                    )
                #End if

            elif choice == 7:
                student_id = student_io.read_student_id("ID of the student: ")
                course_id = result_io.read_course_id()
                semester = result_io.read_semester()
                # VI: Chọn 7: xóa một kết quả, xác định bằng bộ ba mã SV, mã môn, kỳ học.
                result_manager.delete_result(student_id, course_id, semester)
                result_io.show_message("Deleted the result.")
            #End if

        # VI: Lỗi do ResultManager ném (vd không tìm thấy, trùng kết quả): hiện thông báo rồi quay lại menu.
        except ResultManagerException as error:
            result_io.show_message("Error: " + str(error))
        except ValueError as error:
            result_io.show_message("Wrong value: " + str(error))
        #End try
    #End while
#End def


# VI: Lưu cả hai file dữ liệu. Lỗi file của một trong hai bên (FileIOException) thì báo lỗi, không sập chương trình.
def save_all(student_manager: StudentManager, result_manager: ResultManager) -> None:
    """Writes both data files and reports what happened."""
    try:
        student_manager.save_data()
        result_manager.save_data()
        print("Saved every change to file.")
    # VI: Hai FileIOException cùng tên nhưng ở hai file khác nhau, nên được import với bí danh (as) để phân biệt.
    except (StudentFileIOException, ResultFileIOException) as error:
        print("Cannot save: " + str(error))
    #End try
#End def


# VI: Hàm chính: tạo các đối tượng, nạp dữ liệu từ file, chạy vòng lặp menu chính, lưu khi thoát.
def main() -> None:
    """Entry point: loads the data, runs the main menu, saves on exit."""
    student_manager = StudentManager()
    result_manager = ResultManager()
    student_io = StudentConsoleIO()
    result_io = ResultConsoleIO()

    try:
        # VI: Nạp dữ liệu từ file lúc khởi động. File chưa có thì danh sách rỗng, không phải lỗi.
        student_count = student_manager.load_data()
        result_count = result_manager.load_data()
        print("Loaded " + str(student_count) + " student(s) and " + str(result_count) + " result(s).")
    except (StudentFileIOException, ResultFileIOException) as error:
        print("Cannot load the data: " + str(error))
    #End try

    while True:
        show_main_menu()
        # VI: Menu chính chỉ nhận 0 đến 3.
        choice = student_io.read_menu_choice(0, 3)

        if choice == 1:
            run_student_menu(student_manager, student_io, result_manager)
        elif choice == 2:
            run_result_menu(result_manager, result_io, student_manager, student_io)
        elif choice == 3:
            save_all(student_manager, result_manager)
        elif choice == 0:
            save_all(student_manager, result_manager)
            print("Goodbye.")
            return
        #End if
    #End while
#End def


# VI: Chỉ chạy main() khi file được chạy trực tiếp, không chạy khi bị import.
if __name__ == "__main__":
    main()
#End if
