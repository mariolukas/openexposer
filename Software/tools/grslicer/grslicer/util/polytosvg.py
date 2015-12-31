"""
Simple utility for drawing polygons
"""
import tempfile
import webbrowser
import colorsys

import numpy as np

from grslicer.util.np import to_ndarray, get_aabb


class Container(object):
    def __init__(self, size=None, outputfile=None):
        self.inputs = []
        self.size = size or (400, 400)
        self.outputfile = outputfile

    def add(self, title=None, contours=None, lines=None, polylines=None):
        self.inputs.append((title, convert(contours=contours, lines=lines, polylines=polylines)))

    def show(self):
        with tempfile.NamedTemporaryFile(mode='w+t', suffix='.html', delete=False) as f:
            f.write("<!DOCTYPE html>")
            f.write("\n<html>")
            f.write("\n<body>")

            for title, svg in self.inputs:
                f.write("\n<h1>{}</h1>\n".format(title))
                f.write(svg)

            f.write("\n</body>")
            f.write("\n</html>")
            f.seek(0)
            webbrowser.get('firefox').open_new_tab('file://' + f.name)


def convert(contours=None, lines=None, polylines=None, outputfile=None, display=False):
    lines = _get_list(lines)
    contours = _get_list(contours)
    polylines = _get_list(polylines)
    all_elements = [lines, contours, polylines]
    all_l = sum(len(l) for l in all_elements)
    colors = _get_colors(all_l)
    info = {}

    text_width = 120
    default_width = text_width + 15 * all_l
    line_height = 15
    extra_height = 3 * line_height

    aabb = get_aabb(np.concatenate([np.concatenate(x) for x in
                                    all_elements if len(x) > 0]))

    add_x = -aabb.min[0]
    add_y = -aabb.min[1]

    add_v = to_ndarray([add_x, add_y])

    result = "\n<svg width=\"800\" height=\"600\" viewbox=\"{} {} {} {}\">".format(
        0, 0,
        int(aabb.max[0] - aabb.min[0]) + 10, int(aabb.max[1] - aabb.min[1]) + 10)

    for contour in contours:
        contour = contour + add_v
        color = colors.pop()
        result += "\n\t<polygon points=\"{}\" style=\"fill:none;stroke:{};stroke-width:0.1\" />".format(
            _format_polygon(contour), color)
        info.setdefault('Contours', []).append(color)

    for line in lines:
        line = line + add_v
        color = colors.pop()
        result += "\n\t<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\" style=\"stroke:{};stroke-width:0.1\" />".format(
            line[0][0], line[0][1], line[-1][0], line[-1][1], color)
        info.setdefault('Lines', []).append(color)

    for polyline in polylines:
        polyline = polyline + add_v
        color = colors.pop()
        result += "\n\t<polyline points=\"{}\" style=\"fill:none;stroke:{};stroke-width:0.1\" />".format(
            _format_polygon(polyline), color)
        info.setdefault('Polylines', []).append(color)
    result += "\n</svg>"
    result += "\n<br /><svg width=\"{}\" height=\"{}\">".format(default_width, extra_height)
    i = 0
    for k, v in info.items():
        x, y = 0, extra_height - (i * line_height)
        result += "\n\t<text x=\"{}\" y=\"{}\" font-family=\"sans-serif\" font-size=\"{}\" fill=\"black\">{} ({})</text>".format(
            x, y, line_height, k, len(v))

        for j, color in enumerate(v):
            result += "\n\t<rect x=\"{}\" y=\"{}\" width=\"10\" height=\"10\" style=\"fill:{};stroke-width:0;\"/>".format(
                text_width + (j * 15), y - 10, color)
        i += 1
    result += "\n</svg>"

    return result


def _get_list(coll):
    result = []
    _get_list_rec(coll, result)
    return result


def _get_list_rec(coll, result):
    if coll is None or len(coll) is 0:
        return
    if len(coll[0]) > 0:
        if hasattr(coll[0][0], '__iter__'):
            for c in coll:
                _get_list_rec(c, result)
        else:
            result.append(coll)


def _format_polygon(poly):
    return ' '.join(map(lambda x: '' + ','.join(map(str, x)), poly))


def _get_colors(n):
    return ["#" + "".join(
        map(lambda rgb_x: chr(int(rgb_x * 255)).encode('hex'), colorsys.hsv_to_rgb(i * 1.0 / n, 0.9, 0.9)))
            for i in range(n)]

