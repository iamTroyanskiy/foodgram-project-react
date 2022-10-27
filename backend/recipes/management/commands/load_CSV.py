import csv

from .base import CustomCommand


class Command(CustomCommand):
    FILE_EXTENSION = 'CSV'

    def get_rows(self, file):
        return csv.DictReader(
            file,
            fieldnames=self.FIELDS
        )
