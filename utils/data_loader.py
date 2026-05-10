import json
from pathlib import Path


class DataLoader:

    @staticmethod
    def load_test_data(file_name):

        file_path = Path("test_data") / file_name

        with open(file_path, "r") as file:
            return json.load(file)