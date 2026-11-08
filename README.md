# Student Management System

PFP191 Final Project, Topic 4. Group 01, class IA2102, FPT University.

A console program in Python that keeps student profiles and course grades in two text files. The Academic Officer adds, updates and filters students. The Lecturer adds and updates grades, searches the courses of one student, sorts results by status, lists who passed and works out a GPA weighted by credits.

## How to run

Python 3.10 or newer, standard library only.

```
python3 Main.py          # start the program
python3 Test_system.py   # run the 49 unit tests
```

## Files

The code follows three layers and is split into five packages, one class per file.

| Package | Layer | Files |
|---|---|---|
| (top of the folder) | Console IO, tests | Main.py, Test_system.py |
| presentation/ | Console IO | Student_io.py, Result_io.py |
| services/ | Manager | Student_manager.py, Result_manager.py |
| utils/ | Validator | Student_validator.py, Result_validator.py |
| data_access/ | File helper | Student_file_helper.py, Result_file_helper.py |
| models/ | Entity | Person.py, Student.py, Result.py |

Test_system.py uses the _test_data folder, never the real data files. The data files students_data.txt and results_data.txt separate fields with the \| sign.

A result is Pass when the final exam grade is 5 or more, or when it is below 5 and the re-exam grade is 5 or more.
