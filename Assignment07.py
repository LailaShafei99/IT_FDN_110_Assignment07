Python 3.13.0 (v3.13.0:60403a5409f, Oct  7 2024, 00:37:40) [Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   LShafei, 25/11/2024, Completing assignment 7
# ------------------------------------------------------------------------------------------ #
import json

from Assignments.Assignment04 import course_name
from Assignments.Assignment05V2 import last_name

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"


class Person:
    def __init__(self, first_name: str, last_name: str):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self) -> str:
        """
        Return the first name of the person.
        :return: The first name, properly formatted.
        """
        return self._first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Sets the first name, while doing validations.
        :param value: The value to set.
        """
        if value.isalpha():
            self._first_name = value
        else:
            raise ValueError("First name must be alphabetic.")

    @property
    def last_name(self) -> str:
        """
        Return the last name of the person.
        :return: The last name, properly formatted.
        """
        return self._last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Sets the last name, while doing validations.
        :param value: The value to set.
        """
        if value.isalpha():
            self._last_name = value
        else:
            raise ValueError("Last name must be alphabetic.")

    def __str__(self) -> str:
        """
        The string function for Person.
        :return: The string as CSV value.
        """
        return f'{self.first_name}, {self.last_name}'


class Student(Person):
    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        """
        Return the name of the course.
        :return: The name of the course.
        """
        return self._course_name

    @course_name.setter
    def course_name(self, value: str) -> None:
        self._course_name = value

    def __str__(self) -> str:
        """
        The string function for Student.
        :return: The string as CSV value.
        """
        return f'{super().__str__()}, {self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files.

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list[Student]) -> list[Student]:
        """
        This function reads data from a JSON file and loads it into a list of dictionary rows.

        :param file_name: Name of file to read from.
        :param student_data: List of dictionary rows to be filled with file data.

        :return: list
        """
        file_data = []
        file = None
        try:
            file = open(file_name, "r")
            file_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file is not None and not file.closed:
                file.close()

        for row in file_data:
            if "first_name" in row and "last_name" in row and "course_name" in row:
                student_data.append(Student(row["first_name"], row["last_name"], row["course_name"]))
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[Student]) -> None:
        """
        This function writes data to a JSON file with data from a list of dictionary rows.

        :param file_name: Name of file to write to.
        :param student_data: List of dictionary rows to be written to the file.

        :return: None
        """
        file_data = []
        for student in student_data:
            file_data.append({'first_name': student.first_name, 'last_name': student.last_name, 'course_name': student.course_name})

        file = None
        try:
            file = open(file_name, "w")
            json.dump(file_data, file)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output.

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None) -> None:
        """ This function displays custom error messages to the user. """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str) -> None:
        """ This function displays the menu of choices to the user. """
        print(menu)

    @staticmethod
    def input_menu_choice() -> str:
        """ This function gets a menu choice from the user. """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4.")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list[Student]) -> None:
        """ This function displays the student and course names to the user. """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}.')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list[Student]) -> list[Student]:
        """ This function gets the student's first name, last name, and course name from the user. """
        try:
...             student_first_name = input("Enter the student's first name: ")
...             student_last_name = input("Enter the student's last name: ")
...             course_name = input("Please enter the name of the course: ")
...             student = Student(student_first_name, student_last_name, course_name)
...             student_data.append(student)
...             print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
...         except ValueError as e:
...             IO.output_error_messages(message="One of the values was not the correct type of data!", error=e)
...         except Exception as e:
...             IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
...         return student_data
... 
... 
... # Define the Data Variables
... students: list[Student] = []  # A table of student data.
... menu_choice: str  # Holds the choice made by the user.
... 
... # Main body of the script
... students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)
... while True:
...     IO.output_menu(menu=MENU)
...     menu_choice = IO.input_menu_choice()
...     if menu_choice == "1":
...         students = IO.input_student_data(student_data=students)
...     elif menu_choice == "2":
...         IO.output_student_and_course_names(students)
...     elif menu_choice == "3":
...         FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
...     elif menu_choice == "4":
...         break
...     else:
...         print("Please only choose option 1, 2, 3, or 4.")
... print("Program Ended")
