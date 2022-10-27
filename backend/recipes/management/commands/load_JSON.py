import json

from .base import CustomCommand


class Command(CustomCommand):
    FILE_EXTENSION = 'CSV'

    def get_rows(self, file):
        return json.loads(file.read())
