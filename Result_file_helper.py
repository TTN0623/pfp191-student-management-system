# Result_file_helper.py
from Result import Result


class FileIOException(Exception):
    """Raised when the program cannot read or write the result data file."""
    pass
#End class


class ResultFileHelper:
    """
    Reads and writes the result data file.
    This class is the only place that touches results_data.txt
    """
    __FILENAME = "results_data.txt"
    __FIELD_COUNT = 7

    def save(self, result_list: list) -> None:
        """Writes every result of the list to the data file, one result per line."""
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
                    result = self.__parse_line(line)
                    if result is not None:
                        result_list.append(result)
                    #End if
                #End for
            #End with
        except FileNotFoundError:
            return result_list
        except OSError as error:
            raise FileIOException("Cannot read the result file: " + str(error))
        #End try
        return result_list
    #End def

    def __parse_line(self, line: str) -> Result:
        """Turns one line of the file into a Result object, or None when the line is broken."""
        field_list = line.split("|")
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
