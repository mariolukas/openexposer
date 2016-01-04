import numpy as np
from quadtree import Quadtree

from grslicer.util.np import get_aabb, to_ndarray, euclidean_dist_square, closest_point_on_edge


POINT_AABB = to_ndarray([[-10, -10], [10, 10]])


def follow(paths, get_start_func, closed=True):
    """ Iterate through paths as they follow by closeness. Yields
    the closest path that starts on the closest point, and the
    ending point of the path.
    """
    if len(paths) is 0:
        # TODO: check this
        return

    tree, segment_mapping = _get_tree(paths, closed)

    todo_path_mapping = dict([(id(path), path) for path in paths])

    while len(todo_path_mapping) > 0:
        path, path_id = _query(tree, segment_mapping, get_start_func(), todo_path_mapping)

        del todo_path_mapping[path_id]

        if closed:
            start = path[0]
        else:
            start = path[-1]
        yield path, start


def follow_objs(paths, get_start_func, objects, closed=True):
    if len(paths) is 0:
        # TODO: check this
        return

    tree, segment_mapping = _get_tree(paths, closed)
    todo_path_mapping = dict([(id(path), path) for path in paths])
    object_mapping = dict([(id(path), objects[i]) for i, path in enumerate(paths)])

    while len(todo_path_mapping) > 0:
        _, path_id = _query(tree, segment_mapping, get_start_func(), todo_path_mapping, order_path=False)

        del todo_path_mapping[path_id]

        yield object_mapping[path_id]


def _query(tree, mapping, point, paths_dict, order_path=True, scaling=1):
    aabb = (point + (POINT_AABB * scaling)).ravel()

    intersect = tree.likely_intersection(aabb)
    valid_segments = [mapping[map_id] for map_id in intersect if mapping[map_id][0] in paths_dict]

    if valid_segments:
        return _closest_path(valid_segments, point, paths_dict, order_path)

    # increase search perimeter and query again
    return _query(tree, mapping, point, paths_dict, order_path, scaling + 1)


def _closest_path(segments, point, paths_dict, order_path):
    min_path, min_point, min_point_id, min_d, min_segment = None, None, None, None, None
    for segment in segments:
        path = paths_dict[segment[0]]
        point_id = None
        if _is_closed_segment(segment):
            # segment
            p, d, point_id = closest_point_on_edge(path[segment[1]], path[segment[2]], point)
        else:
            # point
            p = path[segment[1]]
            d = euclidean_dist_square(p, point)
        if min_d is None or d < min_d:
            min_path, min_point, min_d, min_segment, min_point_id = path, p, d, segment, point_id

    if order_path:
        if _is_closed_segment(min_segment):
            if min_point_id is 2:
                # order contour so that the projection point is the starting point
                min_path = np.concatenate((to_ndarray([min_point]),
                                           min_path[min_segment[2]:],
                                           min_path[:min_segment[2]]))
            else:
                # closest point is part of the path, rotate the path
                # around that point
                if min_segment[1] is 0:
                    # proper contour start, do nothing
                    pass
                else:
                    min_path = np.roll(min_path, min_segment[min_point_id], axis=0)

        elif min_segment[1] < 0:
            # reverse open path if it ends on the end point denoted as -1
            min_path = min_path[::-1]

    return min_path, min_segment[0]


def _is_closed_segment(segment):
    return len(segment) is 3


def _get_tree(paths, closed):
    """ Add all paths to the tree and create mapping from ids of elements added to the
    tree to the elements data:
    Closed paths:
        [id of path, 1st point of segment, 2nd point of segment]
    Open paths
        [id of path, point of segment]
    """

    # TODO: use models aabb?
    aabb = get_aabb(np.concatenate(paths))
    tree = Quadtree([aabb.min[0], aabb.min[1], aabb.max[0], aabb.max[1]])
    mapping = {}

    for path in paths:
        if closed:
            for i, j in zip(range(-1, len(path) - 1), range(len(path))):
                # add whole edge into the tree
                _add_edge(tree, mapping, path, i, j)

        else:
            _add_point(tree, mapping, path, 0)
            _add_point(tree, mapping, path, -1)

    tree.prune()
    return tree, mapping


def _add_point(tree, mapping, path, point_id):
    """ Add point to the tree. AABB is point itself (2 coordinates)
    """
    map_id = len(mapping)
    mapping[map_id] = (id(path), point_id)
    tree.add(map_id, path[point_id])


def _add_edge(tree, mapping, path, point_from_id, point_to_id):
    """ Add edge to the tree. AABB points are simply points of the edge.
    """

    map_id = len(mapping)

    point_from, point_to = path[point_from_id], path[point_to_id]
    aabb = [
        min(point_from[0], point_to[0]),
        min(point_from[1], point_to[1]),
        max(point_from[0], point_to[0]),
        max(point_from[1], point_to[1])]

    mapping[map_id] = (id(path), point_from_id, point_to_id)
    tree.add(map_id, aabb)
