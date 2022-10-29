import os
import sys

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient


class CustomCommand(BaseCommand):
    FILE_EXTENSION = None
    FIELDS = ['name', 'measurement_unit']

    help = f'Загружает ингредиенты из {FILE_EXTENSION} файла.'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        file_path = os.path.normpath(options["path"])
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                rows_reader = self.get_rows(file)
                for line, row in enumerate(rows_reader):
                    try:
                        Ingredient.objects.create(
                            name=row['name'].capitalize(),
                            measurement_unit=row['measurement_unit'].lower()
                        )
                    except IntegrityError as err:
                        self.stdout.write(f'Line: {line + 1} | Error! {err}')
                self.stdout.write(f'Файл {file_path} загружен!')
        except OSError:
            print(f'OS-error при попытке открыть {file_path}!')
            sys.exit(1)
        except Exception as err:
            print(f"Unexpected error opening {file_path} is", repr(err))
            sys.exit(1)

    def get_rows(self, file):
        pass
