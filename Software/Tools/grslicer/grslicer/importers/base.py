from grslicer.util.progress import progress_log


class ModelImporter(object):
    """
        Interface for importers
    """

    def __init__(self, contents, settings):
        self.contents = contents
        self.merger = None
        self.settings = settings

    @staticmethod
    def can_import(contents):
        return False

    @progress_log('Importing file contents')
    def import_contents(self, progress):
        pass
