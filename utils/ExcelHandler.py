import pandas as pd
from openpyxl import Workbook


class ExcelHandler:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = None

    def create_excel(self, data, sheet_name='Sheet1'):
        """
        Create a new Excel file with the given data.

        Args:
        - data (dict): The data to write to the Excel file. Keys are column names, values are lists of column data.
        - sheet_name (str): The sheet name.
        """
        df = pd.DataFrame(data)
        with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    def read_excel(self, file_path=None, sheet_name='Sheet1'):
        """
        Read data from an Excel file.

        Args:
        - file_path (str): Path to the Excel file. If not provided, the initialized file_path will be used.
        - sheet_name (str): The sheet name to read from.
        """
        if not file_path:
            file_path = self.file_path
        if not file_path:
            raise ValueError("File path must be specified.")

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            self.data = df
            return df
        except Exception as e:
            print(f"Failed to read Excel file. Error: {e}")
            return None

    def edit_excel(self, file_path=None, sheet_name='Sheet1', data=None):
        """
        Edit an existing Excel file, or an in-memory data frame.

        Args:
        - file_path (str): Path to the Excel file. If not provided, the initialized file_path will be used.
        - sheet_name (str): The sheet name to write to.
        - data (dict): The data to write to the Excel file. Keys are column names, values are lists of column data.
        """
        if not file_path:
            file_path = self.file_path
        if not file_path:
            raise ValueError("File path must be specified.")

        if data:
            df = pd.DataFrame(data)
        elif self.data is not None:
            df = self.data
        else:
            raise ValueError("No data provided to edit Excel file.")

        try:
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            print(f"Failed to edit Excel file. Error: {e}")