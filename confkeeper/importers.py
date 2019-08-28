import logging
import os
import shutil
import sys
import tarfile

from . import formatters


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


class TarGzFileImporter(BaseImporter):
    def __init__(self, input_file='confkeeper-export.tar.gz'):
        self.input_file = input_file

    def import_files(self):
        self._uncompress_tar(self.input_file)
        tar_path = self._get_uncompressed_dir(self.input_file)
        metadata = self._get_metadata(tar_path)
        self._copy_files(tar_path, metadata)
        self._remove_uncompressed_tar(tar_path)

    def _uncompress_tar(self, tar_file):
        with tarfile.open(tar_file, 'r:gz') as tar:
            tar.extractall()

    def _get_uncompressed_dir(self, tar_file):
        with tarfile.open(tar_file, 'r:gz') as tar:
            tar_path = tar.getnames()[0]

        return tar_path

    def _get_metadata(self, tar_path):
        metadata_path = self._get_metadata_path(tar_path)
        formatter = formatters.JSONFormatter()

        with open(metadata_path) as fd:
            metadata = formatter.convert_from_format(fd.read())

        return metadata

    def _get_metadata_path(self, tar_path):
        return os.path.join(tar_path, 'metadata.json')

    def _copy_files(self, tar_path, metadata):
        for file_metadata in metadata:
            copied_path = os.path.join(tar_path, file_metadata['copied_path'])
            original_path = os.path.expanduser(file_metadata['original_path'])
            shutil.copy2(copied_path, original_path)

    def _remove_uncompressed_tar(self, tar_path):
        shutil.rmtree(tar_path)
