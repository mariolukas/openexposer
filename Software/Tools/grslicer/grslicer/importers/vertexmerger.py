import spatialhashtable as sht
import grslicer.model as gm


class VertexMerger(object):
    """
        Constructs a topologically connected model based
        on a bucket of vertices and faces.
    """

    def __init__(self, tm, cell_size):
        self.tm = tm
        self.sh = sht.SpatialHash(cell_size)
        self._current_face = None
        self._current_tmp_vertices = None
        self._last_face = None

    def add(self, vector):
        if self._current_face is None:
            self._current_face = gm.TopoFace(model=self.tm)
            self._current_tmp_vertices = []

        face = self._current_face  # make it shorter

        vertex = self.sh.find_equal(vector) or gm.TopoVertex(model=self.tm)

        face.add_vertex(vertex)
        self._current_tmp_vertices.append((vertex, vector))

        # check if currently constructed face has already enough vertices
        if len(self._current_tmp_vertices) is 3:

            # is the face properly constructed or does a face with same vertices
            # exists
            if face.has_unique_vertices() and not face.has_shared_faces():
                self.tm.add_face(face)

                for vertex, vector in self._current_tmp_vertices:

                    vertex.add_face(face)

                    if not self.tm.is_connected(vertex):
                        self.tm.add_vertex(vertex, vector)
                        self.sh.add(vertex)

                vertices = list(face.vertices)
                # check edges of a face
                for vi, vj in ((0, 1), (1, 2), (0, 2)):
                    vertex_1 = vertices[vi]
                    vertex_2 = vertices[vj]

                    edge = vertex_1.get_shared_edge(vertex_2)
                    if edge is None:
                        edge = gm.TopoEdge(model=self.tm)

                        edge.add_vertex(vertex_1)
                        edge.add_vertex(vertex_2)

                        self.tm.add_edge(edge)

                    edge.add_face(face)
                    face.add_edge(edge)
                    vertex_1.add_edge(edge)
                    vertex_2.add_edge(edge)

            # reset for the next face
            self._last_face = self._current_face
            self._current_face = None

    def set_last_face_normal(self, normal):
        self._last_face.normal = normal

    def finalize(self):
        self.tm.purge_mx()
