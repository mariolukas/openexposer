from grslicer.util.np import rotate_xy, np_range, euclidean_dist_square, to_ndarray, euclidean_dist
from grslicer.clipper import pyclipperutil as pcu


def execute(delta, theta, center, max_connection_dist, contours, lines):
    # rotate contours in the opposite direction, so that we
    # process lines that are aligned with x and y axes
    neg_rot_contours = []
    for contour in contours:
        neg_rot_contours.append(rotate_xy(contour, -theta, center))

    lines = pcu.clip_lines(lines, neg_rot_contours)

    lines = _connect_lines(lines, delta, theta, center, max_connection_dist)

    return lines


def get_aabb_lines(aabb, delta):
    # get max aabb for this area so that it is independent
    # of rotation
    d = euclidean_dist(aabb.center[:2], aabb.max[:2])
    min_v, max_v = aabb.min - d, aabb.max + d

    x_l, x_r = min_v[0], max_v[0]

    y_positions = np_range(min_v[1], max_v[1], delta)

    lines = []
    for y in y_positions:
        lines.append(to_ndarray([[x_l, y], [x_r, y]]))

    return lines


def _connect_lines(lines, delta, theta, center, max_connection_dist):
    # lines are np arrays of np arrays tha represent vertices
    connected_lines = []

    # lines should be aligned left-right and be parallel to X-axis
    lines_by_y = {}
    d_lines = []
    for line in lines:

        # align left to right
        if line[0][0] > line[-1][0]:
            line = line[::-1]

        # line should be a list of np arrays that represent vertices
        line = list(line)
        d_lines.append(line)
        lines_by_y.setdefault(line[0][1], []).append(line)

    y_positions = sorted(lines_by_y.keys())
    dist_squared = max_connection_dist ** 2

    while len(lines_by_y) > 0:
        prev_y = y_positions[0]

        # line has to be a list, not a np array
        # because points will be added to it
        line = lines_by_y[prev_y].pop()

        # used y-positions to be removed from line collections
        used_ys = [prev_y]

        for y in y_positions[1:]:
            if not prev_y < y < prev_y + (2 * delta):  # > prev_y and np.isclose(y, prev_y + delta):
                break

            # find if any of lines at the next y is close enough to connect
            next_line_connection_side = 0 if ((len(line) % 4) is 0) else -1
            current_line_connection_vertex = line[-1]

            for line_idx, l in enumerate(lines_by_y[y]):
                next_line_vertex = l[next_line_connection_side]

                # TODO: maybe do a clip in the square between points and if resulting number of polygons
                # is 1 than we cont need the euclidean dist -> just put that polygon into line
                if euclidean_dist_square(current_line_connection_vertex, next_line_vertex) < dist_squared:

                    del lines_by_y[y][line_idx]
                    used_ys.append(y)

                    # properly orient the line
                    if next_line_connection_side is -1:
                        l = l[::-1]
                    line.extend(list(l))

                    # go for next y position
                    break

            prev_y = y

        for y in used_ys:
            if len(lines_by_y[y]) is 0:
                del lines_by_y[y]
                y_positions.remove(y)

        # convert back to np array
        connected_lines.append(rotate_xy(to_ndarray(line), theta, center))
    return connected_lines

