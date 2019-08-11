import logging
import os
import sys


logger = logging.getLogger(__name__)


class BaseImporter:
    def __init__(self, formatter):
        self.formatter = formatter

    def import_files(self, input):
        program_configurations = self.formatter.convert_from_format(input)

        for program, configuration in program_configurations.items():
            logger.debug(f'Importing "{program}" configuration files')
            self.import_program_files(configuration)

    def import_program_files(self, configurations):
        for path, content in configurations.items():
            self.import_file(path, content)

    def import_file(self, path, content):
        with open(os.path.expanduser(path), 'w') as f:
            f.write(content)


class StandardInputImporter(BaseImporter):
    def import_files(self):
        program_configurations = sys.stdin.read()
        super().import_files(program_configurations)


class DryStandardInputImporter(StandardInputImporter):
    def import_file(self, path, content):
        print(path)


class FileImporter(BaseImporter):
    def __init__(self, path, formatter):
        super().__init__(formatter)
        self.path = path

    def import_files(self):
        with open(self.path) as f:
            program_configurations = f.read()

        super().import_files(program_configurations)


class DryFileImporter(FileImporter):
    def import_file(self, path, content):
        print(path)
