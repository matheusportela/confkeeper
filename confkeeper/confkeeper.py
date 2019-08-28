import logging

import click

from . import formatters
from . import importers
from . import exporters


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """Export and import configuration files.

    confkeeper automatically detects configuration files from common programs,
    such as vim or zsh, and serialize them into a format that can be later used
    to restore these configuration files.

    confkeeper also imports configuration files that were previously exported to
    easily restore them.
    """

@click.command(
    name='export',
    short_help='export configurations to be imported in the future')
@click.option(
    '--tar', '-t', is_flag=True, default=False,
    help='export to compressed tarball')
@click.option(
    '--output', '-o', 'output_path', metavar='FILE',
    help='file to export configurations to')
@click.option(
    '--format', '-f',
    type=click.Choice(list(formatters.formatters.keys())), default='json',
    help='file format to export/import')
@click.option(
    '--dry-run', is_flag=True, default=False,
    help='print all files recognized by confkeeper')
def execute_export(tar, output_path, format, dry_run):
    """Export configurations to be imported in the future. Outputs to standard
    output by default.
    """
    formatter = create_formatter(format)
    exporter = create_exporter(formatter, tar, output_path, dry_run)
    exporter.export_files()
cli.add_command(execute_export)

@click.command(
    name='import',
    short_help='import configurations that were previously exported')
@click.option(
    '--tar', '-t', is_flag=True, default=False,
    help='import from compressed tarball')
@click.option(
    '--input', '-i', 'input_path', metavar='FILE', help='file to import configurations from')
@click.option(
    '--format', '-f',
    type=click.Choice(list(formatters.formatters.keys())), default='json',
    help='file format to export/import')
@click.option(
    '--dry-run', is_flag=True, default=False,
    help='print all files recognized by confkeeper')
def execute_import(tar, input_path, format, dry_run):
    """Import configurations that were previously exported. Reads from standard
    input by default.
    """
    formatter = create_formatter(format)
    importer = create_importer(formatter, tar, input_path, dry_run)
    importer.import_files()
cli.add_command(execute_import)

def create_formatter(format):
    return formatters.formatters[format]

def create_exporter(formatter, tar, output_path, dry_run):
    if tar:
        if output_path:
            exporter = exporters.TarGzFileExporter(output_path)
        else:
            exporter = exporters.TarGzFileExporter()
    elif output_path:
        exporter = exporters.FileExporter(output_path, formatter)
    elif dry_run:
        exporter = exporters.DryStandardOutputExporter(formatter)
    else:
        exporter = exporters.StandardOutputExporter(formatter)

    logger.debug(f'Using "{exporter.__class__.__name__}" exporter')
    return exporter

def create_importer(formatter, tar, input_path, dry_run):
    if tar:
        if input_path:
            importer = importers.TarGzFileImporter(input_path)
        else:
            importer = importers.TarGzFileImporter()
    elif input_path and dry_run:
        importer = importers.DryFileImporter(input_path, formatter)
    elif input_path:
        importer = importers.FileImporter(input_path, formatter)
    elif dry_run:
        importer = importers.DryStandardInputImporter(formatter)
    else:
        importer = importers.StandardInputImporter(formatter)

    logger.debug(f'Using "{importer.__class__.__name__}" importer')
    return importer


if __name__ == '__main__':
    cli()
