from grslicer.model import Island
from grslicer.patterns import lines as line, offset, skirts
from grslicer.clipper import pyclipperutil as pcu


def fill_layer(layer, contours, settings, model):
    for island_contours in pcu.define_islands(contours):

        # get shrinked contours for the island
        offsets = offset.execute(island_contours, -abs(settings.extrusionWidth / 2))

        if offsets:
            for island_perimeters in pcu.define_islands(offsets[0]):
                island = Island(perimeters=island_perimeters)
                layer.islands.append(island)

                create_patterns(layer, island, settings, model)

    create_skirts(layer, settings, model)


def create_patterns(layer, island, settings, model):
    enough_space = True
    offsets_delta = -abs(settings.extrusionWidth + settings.offsetsDelta)

    if settings.offsetsNr:
        island.print_perimeters = True

        if settings.offsetsNr > 1:
            island.outer_infill = offset.execute(island.perimeters, offsets_delta, settings.offsetsNr - 1)

        if (len(island.outer_infill) + 1) < settings.offsetsNr:
            # there was not enough space for all offsets
            enough_space = False

    if settings.linesEnable and enough_space:

        # check if there is extra room inside the most inner offset to print lines
        # create offsets and check if all of them completed
        nr = max(settings.offsetsMinNrForLines, 1)
        space_offsets = offset.execute(island.inner_perimeter, offsets_delta, nr)
        if len(space_offsets) is nr:
            # enough space for line infill
            delta = settings.linesDelta + settings.extrusionWidth
            max_connection_dist = delta * settings.linesConnectionDistFactor

            if model.cache_lines is None:
                model.cache_lines = line.get_aabb_lines(model.aabb, delta)
            island.inner_infill = line.execute(delta, _get_lines_rotation(layer.seq_nr, settings), model.aabb.center,
                                               max_connection_dist, space_offsets[0], model.cache_lines)


def create_skirts(layer, settings, model):
    if settings.skirtsLayers and layer.seq_nr < settings.skirtsLayers and settings.skirtsOffsetsNr > 0:
        if model.cache_skirts is None:
            model.cache_skirts = skirts.execute(settings.extrusionWidth, settings.skirtsOffsetsNr, model.aabb,
                                                abs(settings.skirtsInitialDelta))
        layer.skirts = model.cache_skirts


def _get_lines_rotation(layer_seq_nr, settings):
    if settings.linesNrLayersForRotation is 0 or settings.linesRotationTheta is 0:
        return 0

    rotation_index = (((layer_seq_nr - 1) // settings.linesNrLayersForRotation) + 1)
    return max(rotation_index * settings.linesRotationTheta, 0) % 180
