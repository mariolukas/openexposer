import cProfile
import pstats

from grslicer.test import TEST_FILES, TEST_SETTINGS, get_gcode_filename
from grslicer.importer import import_file
from grslicer.slicer import slice_model
from grslicer import gcoder
from grslicer.settings import SlicerSettings
from grslicer.util.polytosvg import Container


def profile(fnc, *args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()
    result = fnc(*args, **kwargs)
    stats = pstats.Stats(pr)
    print 'Results for ', fnc
    stats.strip_dirs().sort_stats('tottime').print_stats()
    return result


def visualize(model):
    c = Container()
    for i, layer in model.layers.items():
        contours, lines = [], []
        for island in layer.islands:
            contours.extend(island.offsets)
            lines.append(island.inner_infill)
        c.add(str(layer), contours=contours, polylines=lines)
    c.show()


def import_files():
    tms = []
    for file_path in TEST_FILES.keys():
        tms.append(import_file(file_path))
    return tms


def slice_models(tms, settings):
    lms = []
    for tm in tms:
        lms.append(slice_model(tm, settings))
    return lms


def encode_models(lms, settings):
    gs = []
    for lm in lms:
        settings.gcode = get_gcode_filename()
        gs.append(gcoder.encode(lm, settings))
    return gs


if __name__ == '__main__':
    settings = SlicerSettings(TEST_SETTINGS)
    settings.verbose = False
    tms = profile(import_files)
    lms = profile(slice_models, tms=tms, settings=settings)
    gs = profile(encode_models, lms=lms, settings=settings)
