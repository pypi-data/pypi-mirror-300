import os
from pathlib import Path
from collections import defaultdict


class Reader:
    """
    A class to read files from a specified directory and categorize them by file extension.

    Attributes
    ----------
    path : str
        The directory path to search for files.
    files_map : defaultdict
        A dictionary that maps file extensions to lists of absolute file paths.
    """

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            The directory path to search for files.
        """
        self.path = Path(path).resolve()  # Get absolute path
        self.files_map = defaultdict(list)  # Initialize the files map
        self._collect_files()  # Collect files on initialization

    def _collect_files(self):
        """Collect files from the specified directory and categorize them by extension."""
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = Path(root) / file  # Get absolute file path
                extension = file_path.suffix  # Get file extension
                self.files_map[extension].append(str(file_path))  # Store in the map

    def get_files_by_extension(self, extension):
        """
        Get a list of files for a specific extension.

        Parameters
        ----------
        extension : str
            The file extension to look for (e.g., '.par', '.gp').

        Returns
        -------
        list
            A list of absolute file paths for the specified extension.
        """
        return self.files_map.get(extension, [])

    def get_all_files(self):
        """
        Get all files found in the directory categorized by their extensions.

        Returns
        -------
        dict
            A dictionary of all files categorized by extension.
        """
        return dict(self.files_map)


# Usage example
if __name__ == "__main__":
    reader = Reader(
        "/home/axis/axis/simulations/scat-b15/output-0000/scat-b15"
        # "/home/axis/axis/comb_data"
    )  # Replace with the target directory path
    par_files = reader.get_files_by_extension(".par")
    gp_files = reader.get_files_by_extension(".gp")
    all_files = reader.get_all_files()

    print("PAR Files:", par_files)
    print("GP Files:", gp_files)
    print("All Files by Extension:")
    for ext, files in all_files.items():
        print(f"{ext}:", files)
