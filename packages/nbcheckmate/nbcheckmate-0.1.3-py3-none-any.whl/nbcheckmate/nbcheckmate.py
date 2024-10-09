"""
This module provides functionality for managing and testing functions
and variables from Jupyter notebooks using pytest and dill.

Classes:
    - ResultsTests: A class to save, load, and run tests for variables and functions,
      with support for running pytest and generating result messages.

Dependencies:
    - dill: Used for pickling and unpickling test data.
    - subprocess: Used to execute pytest and capture the test results.
"""
import os
from pathlib import Path
import subprocess
import dill as pickle

class ResultsTests:
    """
    A class to manage and run tests for functions and variables loaded from notebooks.
    The tests are saved as pickle files in a tests directory.

    Attributes:
        name (str): Name of the test or test step.
        variables (dict): Dictionary of variables to test.
        functions (dict): Dictionary of functions to test.
        test_path (Path): Path to the test directory.
        file_path (str): Path to the pickle file where tests are saved.
    """

    def __init__(self, name, **kwargs):
        """
        Initializes an instance of the ResultsTests class.

        Args:
            name (str): Name of the test or step.
            kwargs: Variables or functions to be tested. Functions are automatically identified.
        """
        self.variables = {}
        self.functions = {}
        self.name = name
        self.test_path = self._locate_tests()
        self.file_path = os.path.join(self.test_path, f'test_{self.name}.pkl')

        for key, value in kwargs.items():
            if callable(value):
                self.functions[key]=value
            else :
                self.variables[key]=value

    def _locate_tests(self):
        """
        Locates the directory containing the tests. It checks both the current directory
        and the parent directory if necessary.

        Returns:
            Path: Path to the 'tests' directory.

        Raises:
            NameError: If no 'tests' directory is found.
        """
        # There is two possible locations for the tests directory
        # 1. In the same directory as the notebook
        # 2. In the parent directory of the notebook
        # We will check both locations
        cwd = Path.cwd()
        tests_path = Path(cwd, 'tests') if Path(cwd, 'tests').is_dir() else Path(cwd.parent,'tests')
        if not tests_path.is_dir():
            raise NameError(
                "Could not find /tests directory in any parent folder")
        return tests_path

    def save(self):
        """
        Saves the current instance as a pickle file.
        """
        with open(self.file_path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, file_name):
        """
        Loads a saved test from a pickle file.

        Args:
            file_name (str): Name of the pickle file to load.

        Returns:
            ResultsTests: An instance of ResultsTests loaded from the file.

        Raises:
            NameError: If the 'tests' directory is not found.
        """
        cwd = os.path.join(os.getcwd(), "src")

        while not os.path.isdir(os.path.join(cwd, 'tests')):
            cwd = os.path.dirname(cwd)
            if cwd == os.sep:
                raise NameError(
                    "Could not find /tests directory in any parent folder")

        file_path = os.path.join(cwd, 'tests', file_name)

        with open(file_path, 'rb') as file:
            return pickle.load(file)

    def get_results(self):
        """
        Runs the tests using pytest and returns the results as a string.
        Adds git instructions if the tests pass.

        Returns:
            str: Test results, with an additional message if the tests pass.
        """
        file_path = f"test_{self.name}.py"
        command = ["python3", "-m", "pytest", "-v", "--color=yes", file_path]
        sub_process = subprocess.Popen(command,
                            cwd=self.test_path,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        output, _ = sub_process.communicate(b"")
        result = output.decode("utf-8")

        if not ("FAILED" in result or "ERROR" in result):
            # tests_directory = 'tests'
            # if self.subdir:
            #     tests_directory = f'{tests_directory}/{self.subdir}'
            result = f"""
{result}\n
🔥 Congratulations, you've just completed the {self.name} step! 🔥\n
First, please verify that everything is correct :\n
\033[1;32mgit\033[39m status\n
Then, don't forget to save your progress :\n
\033[1;32mgit\033[39m add {self.file_path}\n
\033[32mgit\033[39m commit -m \033[33m'Completed {self.name} step'\033[39m\n
\033[32mgit\033[39m push origin main
"""

        return result
        