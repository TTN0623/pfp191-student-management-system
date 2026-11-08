# Student_file_helper.py
# VI: Thuộc lớp File helper: nơi duy nhất đọc và ghi students_data.txt.
# VI: Chứa FileIOException và StudentFileHelper.
# VI: Student_manager gọi save() và load() của file này.
from Student import Student


# VI: Exception riêng của chương trình, dùng khi đọc hoặc ghi file bị lỗi hệ thống (OSError).
class FileIOException(Exception):
    """Raised when the program cannot read or write the student data file."""
    pass
#End class


# VI: Lớp đọc/ghi file dữ liệu sinh viên. Mỗi sinh viên một dòng, các trường ngăn cách bằng |.
class StudentFileHelper:
    """
    Reads and writes the student data file.
    This class is the only place that touches students_data.txt
    """
    # Name of the data file. Two leading underscores keep it inside this class.
    # VI: Hai dấu gạch dưới đầu tên làm thuộc tính private của class: bên ngoài không truy cập được.
    __FILENAME = "students_data.txt"
    # Number of fields on one line of the file
    __FIELD_COUNT = 8

    # VI: Ghi cả list Student ra file, ghi đè nội dung cũ. Lỗi file thì ném FileIOException.
    def save(self, student_list: list) -> None:
        """
        Writes every student of the list to the data file, one student per line.
        """
        try:
            # VI: Mode "w" tạo mới hoặc xóa nội dung cũ; with tự đóng file khi xong.
            with open(StudentFileHelper.__FILENAME, "w", encoding="utf-8") as file_out:
                for student in student_list:
                    file_out.write(student.to_file_string() + "\n")
                #End for
            #End with
        except OSError as error:
            raise FileIOException("Cannot write the student file: " + str(error))
        #End try
    #End def

    # VI: Đọc file, trả về list Student. File chưa có thì trả list rỗng. Lỗi đọc khác thì ném FileIOException.
    def load(self) -> list:
        """
        Reads the data file and returns a list of Student objects.
        A missing file is not an error: the program simply starts empty.
        """
        student_list = []
        try:
            with open(StudentFileHelper.__FILENAME, "r", encoding="utf-8") as file_in:
                for line in file_in:
                    line = line.strip()
                    # VI: Bỏ qua dòng trống.
                    if line == "":
                        continue
                    #End if
                    student = self.__parse_line(line)
                    # VI: __parse_line trả None khi dòng hỏng, các dòng hỏng bị bỏ qua, không dừng chương trình.
                    if student is not None:
                        student_list.append(student)
                    #End if
                #End for
            #End with
        # VI: Lần chạy đầu chưa có file: không phải lỗi, chương trình bắt đầu với danh sách rỗng.
        except FileNotFoundError:
            return student_list
        except OSError as error:
            raise FileIOException("Cannot read the student file: " + str(error))
        #End try
        return student_list
    #End def

    # VI: Hàm private: đổi 1 dòng text thành object Student. Dòng sai số trường hoặc sai giá trị thì trả None.
    def __parse_line(self, line: str) -> Student:
        """
        Turns one line of the file into a Student object.
        Returns None when the line is broken, so one bad line
        does not stop the whole program.
        """
        field_list = line.split("|")
        # VI: Dòng phải có đúng 8 trường, thiếu hoặc thừa là dòng hỏng.
        if len(field_list) != StudentFileHelper.__FIELD_COUNT:
            return None
        #End if
        try:
            return Student(
                student_id=field_list[0],
                full_name=field_list[1],
                date_of_birth=field_list[2],
                gender=field_list[3],
                class_name=field_list[4],
                phone=field_list[5],
                email=field_list[6],
                status=field_list[7]
            )
        except ValueError:
            # A line whose status or format is wrong is skipped,
            # so one broken line cannot stop the whole load.
            return None
        #End try
    #End def
#End class
