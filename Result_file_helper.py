# Result_file_helper.py
# VI: Lớp file helper: file này là nơi duy nhất đọc và ghi results_data.txt.
# VI: Chứa FileIOException (lỗi đọc ghi file) và class ResultFileHelper (save, load).
# VI: Dùng class Result để dựng đối tượng; Result_manager.py gọi ResultFileHelper.
from Result import Result


# VI: Exception riêng báo lỗi không đọc hoặc không ghi được file dữ liệu.
class FileIOException(Exception):
    """Raised when the program cannot read or write the result data file."""
    pass
#End class


# VI: Class đọc và ghi file kết quả. Mỗi dòng trong file là một Result, các trường cách nhau bằng dấu |.
class ResultFileHelper:
    """
    Reads and writes the result data file.
    This class is the only place that touches results_data.txt
    """
    # VI: Tên file dữ liệu và số trường cần có trên mỗi dòng (7 trường). Có dấu __ nên chỉ dùng trong class.
    __FILENAME = "results_data.txt"
    __FIELD_COUNT = 7

    # VI: Ghi cả danh sách ra file, mỗi Result một dòng (mở chế độ "w" nên ghi đè nội dung cũ).
    # VI: Ném FileIOException nếu hệ điều hành không cho ghi.
    def save(self, result_list: list) -> None:
        """Writes every result of the list to the data file, one result per line."""
        # VI: Lỗi hệ điều hành (OSError) được đổi thành FileIOException để các lớp trên chỉ cần bắt một loại lỗi.
        try:
            with open(ResultFileHelper.__FILENAME, "w", encoding="utf-8") as file_out:
                for result in result_list:
                    file_out.write(result.to_file_string() + "\n")
                #End for
            #End with
        except OSError as error:
            raise FileIOException("Cannot write the result file: " + str(error))
        #End try
    #End def

    # VI: Đọc file và trả về list các Result. Dòng trống bị bỏ qua, dòng hỏng bị bỏ qua.
    # VI: Ném FileIOException nếu đọc lỗi (trừ trường hợp file không tồn tại).
    def load(self) -> list:
        """
        Reads the data file and returns a list of Result objects.
        A missing file means the program starts with no result.
        """
        result_list = []
        try:
            with open(ResultFileHelper.__FILENAME, "r", encoding="utf-8") as file_in:
                for line in file_in:
                    line = line.strip()
                    if line == "":
                        continue
                    #End if
                    # VI: __parse_line trả None khi dòng hỏng, lúc đó không thêm vào list.
                    result = self.__parse_line(line)
                    if result is not None:
                        result_list.append(result)
                    #End if
                #End for
            #End with
        # VI: Chưa có file là chuyện bình thường (lần chạy đầu), trả list rỗng chứ không báo lỗi.
        except FileNotFoundError:
            return result_list
        except OSError as error:
            raise FileIOException("Cannot read the result file: " + str(error))
        #End try
        return result_list
    #End def

    # VI: Hàm riêng: tách một dòng thành 7 trường rồi dựng Result. Trả None nếu sai số trường, tín chỉ không phải số hoặc điểm sai.
    def __parse_line(self, line: str) -> Result:
        """Turns one line of the file into a Result object, or None when the line is broken."""
        field_list = line.split("|")
        # VI: Sai số trường (không đủ 7) thì coi là dòng hỏng.
        if len(field_list) != ResultFileHelper.__FIELD_COUNT:
            return None
        #End if
        try:
            credits = int(field_list[4])
        except ValueError:
            return None
        #End try
        try:
            return Result(
                student_id=field_list[0],
                course_id=field_list[1],
                course_name=field_list[2],
                semester=field_list[3],
                credits=credits,
                grade_fe=self.__parse_grade(field_list[5]),
                grade_re=self.__parse_grade(field_list[6])
            )
        except ValueError:
            # A grade outside 0 to 10 makes the setter raise, so the line is skipped.
            return None
        #End try
    #End def

    # VI: Hàm riêng: đổi chữ trong file thành điểm float. Trường rỗng hoặc không phải số thì trả None (chưa thi).
    def __parse_grade(self, text_grade: str) -> float:
        """
        An empty field means the student has not taken that exam,
        so the grade becomes None instead of a number.
        """
        text_grade = text_grade.strip()
        if text_grade == "":
            return None
        #End if
        try:
            return float(text_grade)
        except ValueError:
            return None
        #End try
    #End def
#End class
