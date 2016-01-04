""" Slice D3TopoModel with horizontal planes and create contours
"""

from grslicer.model import Layer, LayeredModel, DEFAULT_COORDINATE_TYPE
from grslicer.util.np import np_range, to_ndarray, np
from grslicer.util import cynp
from grslicer.patterns.infill import fill_layer
from grslicer.util.progress import progress_log


class FixedLayerHeightSlicer(object):
    def __init__(self, tm, settings):
        self.tm = tm
        self.s = settings
        self._slicing_positions = None  # should be private
        self._edge_map = {}  # should be private
        self.model = LayeredModel(aabb=tm.aabb)

    def _init_slicing_positions(self):
        """ Returns heights at which model should be sliced. Starts at <layer_height>
        """
        aabb = self.tm.aabb
        self._slicing_positions = np_range(aabb.min[2] + self.s.layerHeight, aabb.max[2], self.s.layerHeight)

    def _init_edge_height_map(self):
        lh = self.s.layerHeight
        bottom = self._slicing_positions[0] - lh
        for edge in self.tm.edges.values():
            h1 = edge.vertex_a.vector[2]
            h2 = edge.vertex_b.vector[2]

            if h1 != h2:
                if h1 > h2:
                    h1, h2 = h2, h1
                # find intersections with slicing positions
                idx_start = int((h1 - bottom) // lh)
                if idx_start > 0:
                    idx_start -= 1
                idx_end = int((h2 - bottom) // lh) + 1
                for h in self._slicing_positions[idx_start:idx_end]:
                    if h1 < h <= h2:
                        self._edge_map.setdefault(h, set()).add(edge.mxid)

    @progress_log('Slicing model with fixed layer heights')
    def slice(self, progress):
        self._init_slicing_positions()

        progress.set_size(len(self._slicing_positions))

        self._init_edge_height_map()

        for i, h in enumerate(sorted(self._edge_map.keys())):

            contours = []

            # edges that need to be visited on this height
            to_visit = self._edge_map[h]
            while len(to_visit) > 0:
                # 2D path - z coordinate is omitted as it is represented as height
                contour = []

                prev_face = None
                edge = self.tm.edges[to_visit.pop()]

                while True:

                    # intersect the edge
                    intersection = _edge_2d_intersection(edge, h)
                    contour.append(intersection)

                    to_visit.discard(edge.mxid)

                    # march
                    if prev_face is None:
                        # doesn't matter which face
                        prev_face = edge.face_a
                    else:
                        # select the opposite from the one we came
                        prev_face = edge.face_b if prev_face is edge.face_a else edge.face_a

                    # select edge from edges of a face that has not yet been worked on
                    edge = next((e for e in prev_face.edges if e.mxid in to_visit), None)

                    # contour is finished when there is no more edges to cut
                    # WARNING: if the topology of the model is not manifold (holes in mesh)
                    # it might happen that the contour will be closed too soon
                    if edge is None:
                        break

                # All contours are closed
                contours.append(to_ndarray(contour))

            if contours:
                self.add_layer(contours, h, i)

            progress.inc()

        progress.done()

    def add_layer(self, contours, height, seq_nr):
        layer = Layer(self.model, height, seq_nr)
        fill_layer(layer, contours, self.s, self.model)
        self.model.layers[seq_nr] = layer


def _edge_2d_intersection(edge, h):
    return cynp.edge_intersection(edge.vertex_a.vector, edge.vertex_b.vector, h)


class ScanlineSlicer(object):
    def __init__(self, tm, settings):
        self.tm = tm
        self.s = settings
        self._slicing_positions = None  # should be private
        self._scanline_positions = None # should be private
        self._face_map = {}  # should be private
        self.model = LayeredModel(aabb=tm.aabb)

    def _init_slicing_positions(self):
        """ Returns heights at which model should be sliced. Starts at <layer_height>
        """
        aabb = self.tm.aabb
        self._slicing_positions = np_range(aabb.min[2] + self.s.layerHeight/2+0.001, aabb.max[2], self.s.layerHeight, endpoint=False)
        self._scanline_positions = np_range(aabb.min[1], aabb.max[1], self.s.scanlineSpacing)

    def _init_face_height_map(self):
        lh = self.s.layerHeight
        bottom = self._slicing_positions[0] - lh
        for face in self.tm.faces.values():
            for edge in face.edges:
                h1 = edge.vertex_a.vector[2]
                h2 = edge.vertex_b.vector[2]

                if h1 != h2:
                    if h1 > h2:
                        h1, h2 = h2, h1
                    # find intersections with slicing positions
                    idx_start = int((h1 - bottom) // lh)
                    if idx_start > 0:
                        idx_start -= 1
                    idx_end = int((h2 - bottom) // lh) + 1
                    for h in self._slicing_positions[idx_start:idx_end]:
                        if h1 <= h <= h2:
                            self._face_map.setdefault(h, set()).add(face.mxid)

    @progress_log('Slicing model with fixed layer heights')
    def slice(self, progress):
        self._init_slicing_positions()

        progress.set_size(len(self._slicing_positions))

        self._init_face_height_map()

        for i, h in enumerate(sorted(self._face_map.keys())):

            lines = []

            # faces that need to be visited on this height
            # 2D path - z coordinate is omitted as it is represented as height
            for scanline_y in self._scanline_positions:


                points = []

                to_visit = self._face_map[h]
                scanline_point = [0, scanline_y, h]
                scanline_direction = [1, 0, 0]

                for face_id in to_visit:
                    face = self.tm.faces[face_id]

                    face_max_y = max(face.vertex_a.vector[1], face.vertex_b.vector[1], face.vertex_c.vector[1])
                    face_min_y = min(face.vertex_a.vector[1], face.vertex_b.vector[1], face.vertex_c.vector[1])

                    if scanline_y <= face_max_y and scanline_y >= face_min_y:

                        result, intersection_point = _intersect_face_line(face, scanline_point, scanline_direction)

                        if result == 2:
                            #print "Line within plane ("+str(face.vertex_a.vector)+"|"+str(face.vertex_b.vector)+"|"+str(face.vertex_c.vector)+")"
                            #print "Testing face "+str(face.mxid)+" with scanline "+str(scanline_point)+" result 2"
                            pass

                        elif result == 1:
                            #print "Testing face "+str(face.mxid)+" with scanline "+str(scanline_point)+" result 1 ("+str(intersection_point)+") direction "+str(direction)

                            points.append(intersection_point)

                        elif result == 0:
                            # print "Testing face "+str(face.mxid)+" with scanline "+str(scanline_point)+" result 0"
                            pass

                        elif result == -1:
                            # print "Testing face "+str(face.mxid)+" with scanline "+str(scanline_point)+" result -1"
                            pass

                if points:
                    points = np.array(points)
                    points = points[points[:,0].argsort()]

                    unique_points = []

                    # All contours are closed
                    for point in points:
                        found = False
                        for other_point in unique_points:
                            if np.linalg.norm(point[0:3]-other_point[0:3]) < 0.0001:
                                found = True
                        if not found:
                            unique_points.append(point)

                    if len(unique_points) == 1:
                        print "only single intersection in line "+str(unique_points)

                    elif len(unique_points) % 2 == 1:
                        print "invalid number of points "+str(unique_points)

                    else:
                        lines.append(unique_points)

            if lines:
                self.add_layer(lines, h, i)

            progress.inc()

        progress.done()

    def add_layer(self, lines, height, seq_nr):
        layer = Layer(self.model, height, seq_nr)
        layer.lines = lines
        self.model.layers[seq_nr] = layer


def _intersect_face_line(face, scanline_point, scanline_direction):
    SMALL_NUM = 0.00000001 # anything that avoids division overflow
    # dot product (3D) which allows vector operations in arguments
    #define dot(u,v)   ((u).x * (v).x + (u).y * (v).y + (u).z * (v).z)
    # intersect3D_RayTriangle(): find the 3D intersection of a ray with a triangle
    #    Input:  a ray R, and a triangle T
    #    Output: *I = intersection point (when it exists)
    #    Return: -1 = triangle is degenerate (a segment or point)
    #             0 =  disjoint (no intersect)
    #             1 =  intersect in unique point I1
    #             2 =  are in the same plane
    # int intersect3D_RayTriangle( Ray R, Triangle T, Point* I )

    #    Vector    u, v, n;              // triangle vectors
    #    Vector    dir, w0, w;           // ray vectors
    #    float     r, a, b;              // params to calc ray-plane intersect

    # get triangle edge vectors and plane normal
    va = face.vertex_a.vector
    vb = face.vertex_b.vector
    vc = face.vertex_c.vector
    u = vb - va #u = T.V1 - T.V0;
    v = vc - va #v = T.V2 - T.V0;
    n2 = np.cross(u, v) #n = u * v;              // cross product
    n = face.normal

    if n[0] == DEFAULT_COORDINATE_TYPE(0) and n[1] == DEFAULT_COORDINATE_TYPE(0) and n[2] == DEFAULT_COORDINATE_TYPE(0): # // triangle is degenerate
        return (-1, None)                   #// do not deal with this case

    dir = to_ndarray(scanline_direction) #dir = R.P1 - R.P0; // ray direction vector
    w0 = to_ndarray(scanline_point) - va # w0 = R.P0 - T.V0;
    a = - np.dot(n, w0) # a = -dot(n,w0);
    b = np.dot(n, dir) # b = dot(n,dir);
    if abs(b) < DEFAULT_COORDINATE_TYPE(SMALL_NUM): #if (fabs(b) < SMALL_NUM) {     // ray is  parallel to triangle plane
        if a == DEFAULT_COORDINATE_TYPE(0): #    if (a == 0)                 // ray lies in triangle plane
            return (2, None)
        else:
            return (0, None) #              // ray disjoint from plane
    # }

    # // get intersect point of ray with triangle plane
    r = a / b # r = a / b;
    if r < DEFAULT_COORDINATE_TYPE(0.0): # if (r < 0.0)                    // ray goes away from triangle
        return (0, None) #                  // => no intersect
    # // for a segment, also test if (r > 1.0) => no intersect

    I = to_ndarray([scanline_point[0]+r, scanline_point[1], scanline_point[2], np.dot(n, dir)/abs(np.dot(n, dir))]) #*I = R.P0 + r * dir;            // intersect point of ray and plane

    # // is I inside T?
    # float    uu, uv, vv, wu, wv, D;
    uu = np.dot(u, u) # uu = dot(u,u);
    uv = np.dot(u, v) # uv = dot(u,v);
    vv = np.dot(v, v) # vv = dot(v,v);
    w = I[0:3] - va # w = *I - T.V0;
    wu = np.dot(w, u) # wu = dot(w,u);
    wv = np.dot(w, v) # wv = dot(w,v);
    D = uv * uv - uu * vv # D = uv * uv - uu * vv;

    if D == DEFAULT_COORDINATE_TYPE(0.0):
        return (0, None)

    # // get and test parametric coords
    # float s, t;
    s = (uv * wv - vv * wu) / D # s = (uv * wv - vv * wu) / D;
    if s < DEFAULT_COORDINATE_TYPE(0.0) or s > DEFAULT_COORDINATE_TYPE(1.0): # if (s < 0.0 || s > 1.0)         // I is outside T
        return (0, None)
    t = (uv * wu - uu * wv) / D # t = (uv * wu - uu * wv) / D;
    if t < DEFAULT_COORDINATE_TYPE(0.0) or (s+t) > DEFAULT_COORDINATE_TYPE(1.0): # if (t < 0.0 || (s + t) > 1.0)  // I is outside T
        return (0, None)

    return (1, I) #                      // I is in T


def slice_model(tm, settings, slicer_class=FixedLayerHeightSlicer):
    slicer = slicer_class(tm, settings)
    slicer.slice()
    return slicer.model
