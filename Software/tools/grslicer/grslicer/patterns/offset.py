from grslicer.clipper import pyclipperutil as pcu


def execute(perimeters, delta, nr=1):
    return pcu.offset_contours(perimeters, delta, nr)
