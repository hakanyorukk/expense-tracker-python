import csv
import json
from abc import ABC, abstractmethod
from json import JSONDecodeError

from expense import StorageError

FIELDS = ["amount", "category", "description", "date"]
class Storage(ABC):

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def load(self):
        pass

class JsonStorage(Storage):
    def __init__(self, filename):
        self.filename=filename

    def save(self, data):
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file)
        except OSError as e:
            raise StorageError(f"Could not write {self.filename}") from e

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise StorageError(f"{self.filename} is not valid JSON") from e
        except OSError as e:
            raise StorageError(f"Could not read {self.filename}") from e

class CsvStorage(Storage):
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):

        try:
            with open(self.filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(data)
        except OSError as e:
            raise StorageError(f"Could not write {self.filename}") from e

    def load(self):
        try:
            with open(self.filename, "r", newline="") as file:
                rows = list(csv.DictReader(file))
        except FileNotFoundError:
            return []
        except OSError as e:
            raise StorageError(f"Could not read {self.filename}") from e

        expenses = []
        for row in rows:
            try:
                expenses.append({
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "description": row.get("description", ""),
                    "date": row["date"],
                })
            except (KeyError, ValueError, TypeError) as e:
                raise StorageError(f"Bad row in {self.filename}: {row}") from e
        return expenses
