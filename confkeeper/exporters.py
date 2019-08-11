import logging
import os
import sys

from . import adapters


class BaseExporter:
    def __init__(self, formatter):
        self.adapters = [
            adapters.VimAdapter(),
            adapters.ZshAdapter(),
        ]
        self.formatter = formatter

    def export_files(self):
        result = {}

        for adapter in self.adapters:
            result[adapter.name()] = dict(adapter.export_files())

        return self.formatter.convert_to_format(result)


class StandardOutputExporter(BaseExporter):
    def export_files(self):
        program_configurations = super().export_files()
        sys.stdout.write(program_configurations)


class FileExporter(BaseExporter):
    def __init__(self, path, formatter):
        super().__init__(formatter)
        self.path = path

    def export_files(self):
        program_configurations = super().export_files()
        with open(os.path.expanduser(self.path), 'w') as f:
            f.write(program_configurations)

class DryStandardOutputExporter(BaseExporter):
    def export_files(self):
        for adapter in self.adapters:
            program = adapter.name()
            files = [file for file, _ in adapter.export_files()]

            for file in files:
                print(file)
