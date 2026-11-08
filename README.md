# Student Management System

PFP191 Final Project, Topic 4. Group 01, class IA2102, FPT University.

A console program in Python that keeps student profiles and course grades in two text files. The Academic Officer adds, updates and filters students. The Lecturer adds and updates grades, searches the courses of one student, sorts results by status, lists who passed and works out a GPA weighted by credits.

## How to run

Python 3.10 or newer, standard library only.

```
python3 Main.py          # start the program
python3 Test_system.py   # run the 47 unit tests
```

## Files

| Layer | Files |
|---|---|
| Console IO | Main.py, Student_io.py, Result_io.py |
| Manager and validator | Student_manager.py, Result_manager.py, Student_validator.py, Result_validator.py |
| File helper | Student_file_helper.py, Result_file_helper.py |
| Entity | Person.py, Student.py, Result.py |
| Tests | Test_system.py (uses the _test_data folder, never the real data files) |
| Data | students_data.txt, results_data.txt (fields separated by the \| sign) |

A result is Pass when the final exam grade is 5 or more, or when it is below 5 and the re-exam grade is 5 or more.
