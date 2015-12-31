from stl import StlAsciiImporter, StlBinImporter
from grslicer.util.progress import progress_log

ALL_IMPORTERS = [StlAsciiImporter, StlBinImporter]


class SlicerImportException(Exception):
    pass


@progress_log('Importing file')
def import_file(file_path, settings, progress):

    progress.set_size(4)

    with open(file_path, 'r') as f:

        contents = read_contents(f)
        progress.inc()

        importer_cls = next((x for x in ALL_IMPORTERS if x.can_import(contents)), None)
        progress.inc()

        importer = importer_cls(contents, settings)
        result = importer.import_contents()

        progress.inc()

        if result is None:
            raise SlicerImportException('The provided file can not be imported')
        else:
            result.center(settings.printPlateWidth, settings.printPlateLength)

    progress.done()

    return result


@progress_log('Reading file')
def read_contents(file_stream, progress):
    progress.set_size(1)

    contents = file_stream.read()

    progress.done()
    return contents