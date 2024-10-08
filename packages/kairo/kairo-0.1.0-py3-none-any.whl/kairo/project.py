"""
This file contains the project manager class.
"""

from os import path, mkdir, rmdir, listdir

from kairo.constants import DEFAULT_PROJECT_DIR


class Manager:
    """
    The project manager class.
    """

    def __init__(self):
        self._project_dir = path.join(path.dirname(path.abspath(__file__)), DEFAULT_PROJECT_DIR)

    def add(self, name: str) -> bool:
        """
        Add a new project to the project directory.
        """
        if not name:
            raise ValueError("Project name cannot be empty.")

        new_project_dir = path.join(self._project_dir, name)
        if path.exists(new_project_dir):
            return False

        mkdir(new_project_dir)

        return True

    def remove(self, name):
        """
        Remove a project from the project directory.
        """
        if not name:
            raise ValueError("Project name cannot be empty.")

        new_project_dir = path.join(self._project_dir, name)
        if not path.exists(new_project_dir):
            return False

        rmdir(new_project_dir)

        return True

    def list(self):
        """
        List all projects in the project directory.
        """
        return [
            d for d in listdir(self._project_dir) if path.isdir(path.join(self._project_dir, d))
        ]
