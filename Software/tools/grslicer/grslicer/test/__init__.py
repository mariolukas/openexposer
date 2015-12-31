import time

from grslicer.settings import SlicerSettings


TEST_FILES = {
    'data/25mm_cube_ascii.stl': {
        'type': 'ascii',
        'nr_vertices': 16,
        'nr_faces': 28,
        'nr_edges': 42,
        'euler': 2,
        'aabb': [25, 25, 25]
    },
    'data/25mm_cube_bin.stl': {
        'type': 'bin',
        'nr_vertices': 16,
        'nr_faces': 28,
        'nr_edges': 42,
        'euler': 2,
        'aabb': [25, 25, 25]
    },
    'data/ctrlV_3D_test.stl': {
        'type': 'bin',
        'nr_vertices': 3331,
        'nr_faces': 6746
    },
}

"""
'data/SPIRAL-02.STL': {
        'type': 'bin',
        'nr_vertices': 51405,
        'nr_faces': 102806,
        'euler': 2
    },
"""


def get_gcode_filename(name=None):
    return get_tm_file('.gcode')


def get_tm_file(ext):
    return '/tmp/' + time.strftime("%Y%m%d-%H%M%S") + ext


TEST_SETTINGS = {
    'layerHeight': 0.25,
    'skirtsInitialDelta': 5,
    'skirtsOffsetsNr': 3,
    'skirtsLayers': 2,
    'linesEnable': True,
    'linesDelta': 0.5,
    'linesConnectionDistFactor': 5,
    'offsetsNr': 3,
    'offsetsDelta': 0,
    'offsetsMinNrForLines': 1
}


def get_test_settings():
    return SlicerSettings(flat_settings_dict=TEST_SETTINGS)


TEST_FILE_CUBE = 'data/25mm_cube_bin.stl'

CONTOUR = ((0, 0), (100, 0), (100, 100), (0, 100))
HOLE = ((20, 20), (80, 20), (80, 80), (20, 80))
INNER_ISLAND = ((40, 40), (60, 40), (60, 60), (40, 60))

TETRAHEDRON_VERTICES = ((1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1))
TETRAHEDRON_FACES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))

ENABLE_VISUALS = True
ENABLE_PROFILER = False



