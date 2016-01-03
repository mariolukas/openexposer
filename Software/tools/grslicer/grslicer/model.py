from collections import OrderedDict

import numpy as np

from grslicer import DEFAULT_COORDINATE_TYPE
from grslicer.util.np import get_aabb, to_ndarray


class Matrix(object):
    """
        Represents an object with a numpy array
    """

    def __init__(self, shape):
        self.mx = np.ndarray(shape=shape, dtype=DEFAULT_COORDINATE_TYPE)
        self._mx_pos = 0

    def add_vector(self, vector):
        self.mx[self._mx_pos] = vector
        self._mx_pos += 1

    @property
    def aabb(self):
        return get_aabb(self.mx)

    def center(self, width, length):
        aabb = self.aabb

        # center X, Y
        x = width / 2.0
        y = length / 2.0
        z = aabb.center[2] - aabb.min[2]
        self.mx += to_ndarray([x, y, z]) - aabb.center


class TopoModel(Matrix):
    def __init__(self, *args, **kwargs):
        super(TopoModel, self).__init__(*args, **kwargs)

        self.vertices = {}
        self.faces = {}
        self.edges = {}

    def get_euler(self):
        f_nr = len(self.faces)
        v_nr = len(self.vertices)
        e_nr = len(self.edges)
        # print "Euler: F + V - E = %i + %i - %i = %i" % (f_nr, v_nr, e_nr, (f_nr + v_nr - e_nr))
        return f_nr + v_nr - e_nr

    def get_vector(self, vertex):
        return self.mx[vertex.mxid]

    @staticmethod
    def is_connected(topo_el):
        return topo_el.mxid is not None

    def purge_mx(self):
        """
            Remove unnecessarily allocated space
        """
        self.mx = np.resize(self.mx, (len(self.vertices), 3))

    def add_vertex(self, vertex, vector):
        """
            Add vertices vector to the inner matrix and mark
            matrix index of vertices vector.
        """
        if vertex.mxid is not None:
            return

        mxid = self._mx_pos
        self.add_vector(vector)
        vertex.mxid = mxid
        self.vertices[mxid] = vertex

    def add_edge(self, edge):

        if edge.mxid is not None:
            return

        edge.mxid = len(self.edges)
        self.edges[edge.mxid] = edge

    def add_face(self, face):

        if face.mxid is not None:
            return

        face.mxid = len(self.faces)
        self.faces[face.mxid] = face


class TopoException(Exception):
    """
    Something is wrong with topology
    """
    pass


class TopoElement(object):
    VERTICES_NR = None
    EDGES_NR = None
    FACES_NR = None
    SHORT_CODE = 'X'

    __slots__ = ['mxid', 'model', 'vertices', 'edges', 'faces']

    def __init__(self, mxid=None, model=None):
        self.mxid = mxid
        self.model = model

        self.vertices = set()
        self.edges = set()
        self.faces = set()

    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        if self.VERTICES_NR is not None and len(self.vertices) > self.VERTICES_NR:
            raise TopoException('To many vertices')

    def add_edge(self, edge):
        self.edges.add(edge)
        if self.EDGES_NR is not None and len(self.edges) > self.EDGES_NR:
            raise TopoException('To many edges')

    def add_face(self, face):
        self.faces.add(face)
        if self.FACES_NR is not None and len(self.faces) > self.FACES_NR:
            raise TopoException('To many faces')

    def __str__(self):
        return '{}{}'.format(self.SHORT_CODE, self.mxid)

    def __repr__(self):
        return '{}{}'.format(self.SHORT_CODE, self.mxid)


class TopoVertex(TopoElement):
    VERTICES_NR = 0
    EDGES_NR = None
    FACES_NR = None
    SHORT_CODE = 'V'

    @property
    def vector(self):
        if not self.model.is_connected(self):
            raise TopoException('Vertex is not connected to the model')

        return self.model.get_vector(self)

    def get_shared_edge(self, vertex):
        shared = self.edges & vertex.edges
        if len(shared) is 1:
            return shared.pop()
        if len(shared) > 1:
            raise TopoException('WARNING: {} and {} share several edges {}'.format(self, vertex, shared))
        return None

    def __repr__(self):
        return super(TopoVertex, self).__repr__() + str(list(self.vector))


class TopoEdge(TopoElement):
    VERTICES_NR = 2
    EDGES_NR = 0
    FACES_NR = 2
    SHORT_CODE = 'E'

    def has_unique_vertices(self):
        return len(self.vertices) is self.VERTICES_NR

    @property
    def vertex_a(self):
        return list(self.vertices)[0]

    @property
    def vertex_b(self):
        return list(self.vertices)[1]

    @property
    def face_a(self):
        return list(self.faces)[0]

    @property
    def face_b(self):
        return list(self.faces)[1]


class TopoFace(TopoEdge):
    VERTICES_NR = 3
    EDGES_NR = 3
    FACES_NR = 0
    SHORT_CODE = 'F'

    def __init__(self, mxid=None, model=None):
        super(TopoFace, self).__init__(mxid=None, model=None)
        self.normal = None

    @property
    def vertex_c(self):
        return list(self.vertices)[2]

    def has_shared_faces(self):
        """
        Check whether vertices contain another equal facet
        """

        faces = [vertex.faces for vertex in self.vertices]

        shared_faces = faces[0].intersection(*faces)

        if self in shared_faces:
            shared_faces.remove(self)

        return len(shared_faces) > 0


class LayeredModel(object):
    def __init__(self, aabb):
        self.layers = OrderedDict()
        self.aabb = aabb
        self.cache_lines = None
        self.cache_skirts = None

    def __str__(self):
        return 'LayeredModel({})'.format(len(self.layers))

    def __repr__(self):
        return self.__str__()


class Layer(object):
    __slots__ = ['model', 'height', 'seq_nr', 'islands', 'skirts', 'lines']

    def __init__(self, model, height, seq_nr):
        self.model = model
        self.height = height
        self.seq_nr = seq_nr  # 0-based

        self.islands = []

        # collection of individual paths
        # sorted from outer to inner
        self.skirts = []

        self.lines = []

    def __str__(self):
        return 'Layer(height={},seq_nr={})'.format(self.height, self.seq_nr)

    def __repr__(self):
        return self.__str__()


class Island(object):
    __slots__ = ['perimeters', 'outer_infill', 'inner_infill', 'print_perimeters']

    def __init__(self, perimeters=None):
        # sorted from outside towards inside
        self.perimeters = [] if perimeters is None else perimeters
        self.outer_infill = []
        self.inner_infill = []
        self.print_perimeters = False

    @property
    def inner_perimeter(self):
        if self.outer_infill:
            return self.outer_infill[-1]
        return self.perimeters

    @property
    def offsets(self):
        offsets = []
        if self.print_perimeters:
            offsets.append(self.perimeters)
        if self.outer_infill:
            offsets.extend(self.outer_infill)

        return offsets

    def __str__(self):
        return 'Island(nr_perimeters={},nr_offsets={},nr_lines={})'.format(len(self.perimeters), len(self.outer_infill),
                                                                           len(self.inner_infill))

    def __repr__(self):
        return self.__str__()
