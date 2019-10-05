import logging
import os
import shutil
import sys
import tarfile
import tempfile

from . import adapters
from . import formatters


class BaseExporter:
    def __init__(self, formatter):
        self.formatter = formatter

    def export_files(self):
        result = {}

        for adapter in adapters.adapters:
            result[adapter.name] = dict(adapter.export_files())

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
        for adapter in adapters.adapters:
            program = adapter.name
            files = [file for file, _ in adapter.export_files()]

            for file in files:
                print(file)

class TarGzFileExporter(BaseExporter):
    def __init__(self, output_file='confkeeper-export.tar.gz'):
        self.output_file = output_file

    def export_files(self):
        program_files = self._get_program_files()

        with tempfile.TemporaryDirectory() as temp_dir:
            self._copy_program_files(program_files, temp_dir)
            self._generate_metadata_file(temp_dir, program_files)
            self._generate_output_file(temp_dir, self.output_file)

    def _get_program_files(self):
        program_files = {}

        for adapter in adapters.adapters:
            program_files[adapter.name] = adapter.paths

        return program_files

    def _copy_program_files(self, program_files, temp_dir):
        for program, file_paths in program_files.items():
            program_path = os.path.join(temp_dir, program)
            os.mkdir(program_path)

            for file_path in file_paths:
                shutil.copy2(os.path.expanduser(file_path), program_path)

    def _generate_metadata_file(self, temp_dir, program_files):
        metadata = self._get_metadata(program_files)
        formatter = formatters.JSONFormatter()

        with open(os.path.join(temp_dir, 'metadata.json'), 'w') as fd:
            fd.write(formatter.convert_to_format(metadata))

    def _get_metadata(self, program_files):
        metadata = []

        for program, file_paths in program_files.items():
            for file_path in file_paths:
                copied_path = os.path.join(program, os.path.basename(file_path))
                original_path = file_path
                metadata.append({
                    'copied_path': copied_path,
                    'original_path': original_path
                })

        return metadata

    def _generate_output_file(self, temp_dir, output_file):
        with tarfile.open(output_file, 'w:gz') as tar:
            tar_dir = output_file.split('.')[0]
            tar.add(temp_dir, arcname=tar_dir)
