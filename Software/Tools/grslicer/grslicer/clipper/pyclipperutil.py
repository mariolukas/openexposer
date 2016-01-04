""" Utility functions for pyclipper
"""

import pyclipper as pc
from grslicer.util.np import to_ndarray

pc.SILENT = True
pc.SCALING_FACTOR = 10000.0


def define_islands(polygons):
    """
    Find groups of polygons that define islands within a list of polygons.

    Returns a collection of island defining groups of polygons. Each group of polygons
    is ordered so that the external polygon is the first in list and has a CCW orientation,
    after that follow polygons that define holes in the external polygon and are oriented
    CW.
    """

    c = pc.Pyclipper()

    c.AddPaths(polygons, poly_type=pc.PT_SUBJECT, closed=True)
    tree = c.Execute2(clip_type=pc.CT_DIFFERENCE)
    groups = []
    _filter_groups_from_poly_node(tree, groups)

    return groups


def offset_contours(polygons, delta, nr=1):
    """ Create offsets of contours """

    pco = pc.PyclipperOffset()
    pco.AddPaths(polygons, pc.JT_MITER, pc.ET_CLOSEDPOLYGON)

    offsets = []

    for i in range(nr):
        offset = _to_ndarrays(pco.Execute(delta * (i + 1)))

        if offset:
            offsets.append(offset)
        else:
            # offsets are not possible anymore
            break

    return offsets


def clip_lines(lines, contours):
    """ Clip lines with contours.
    Return collection of open polygons ordered by y axis
    """
    # TODO simplify lines
    c = pc.Pyclipper()
    c.AddPaths(contours, pc.PT_CLIP)
    c.AddPaths(lines, pc.PT_SUBJECT, False)

    tree = c.Execute2(pc.CT_INTERSECTION)

    paths = pc.OpenPathsFromPolyTree(tree)

    return _to_ndarrays(paths)


def _filter_groups_from_poly_node(tree, groups, is_outer_perimeter=None):
    """ Recursively parses clippers <PyPolyTree> for island contours
    Fills #islands parameter with collections of paths that represent islands.
    Path element is <Point>

    if is_outer_perimeter is None -> we don't know what is it
    The first child that has non-empty .contour is considered as outer perimeter

    """
    if is_outer_perimeter is None:
        is_outer_perimeter = True if tree.Contour else False

    if is_outer_perimeter:

        """
        Structure of the tree:


            [Island root].contour = outer perimeter
                `-> [Island child].contour = inner perimeter
                    `-> [Island root] ...
                `-> [Island child].contour = inner perimeter

        """

        paths = [to_ndarray(tree.Contour)]
        groups.append(paths)
        for child in tree.Childs:
            paths.append(to_ndarray(child.Contour))
            _filter_groups_from_poly_node(child, groups, False)
    else:
        for child in tree.Childs:
            _filter_groups_from_poly_node(child, groups, True)


def _to_ndarrays(clipper_paths):
    paths = []
    for clipper_path in clipper_paths:
        paths.append(to_ndarray(clipper_path))
    return paths
