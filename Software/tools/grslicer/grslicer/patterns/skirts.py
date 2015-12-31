from grslicer.patterns import offset
from grslicer.util.np import to_ndarray


def execute(delta, nr, aabb, initial_delta=0):
    initial_delta += delta * nr
    contour = to_ndarray([(aabb.min - initial_delta)[:2],
                          [aabb.min[0] - initial_delta, aabb.max[1] + initial_delta],
                          (aabb.max + initial_delta)[:2],
                          [aabb.max[0] + initial_delta, aabb.min[1] - initial_delta]])
    offsets = offset.execute([contour], -abs(delta), nr)
    return [o[0] for o in offsets]

