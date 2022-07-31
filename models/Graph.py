class Vertex:
    def __init__(self, label, address):
        self.label = label
        self.address = address
        self.distance = float('inf')
        self.previous_vertex = None


class Graph:
    def __init__(self):
        self.vertices_added = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.vertices_added[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.vertices_added[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def get_vertices(self):
        return self.vertices_added

    def print_vertex_info(self):
        vertex_list = []
        separator = "*******************************************************************************************"
        for vertex in self.vertices_added:
            vertex_info = "(" + str(vertex.label) + ") \t|Dist: " + str(vertex.distance)
            vertex_info = vertex_info + "\t| Address: " + vertex.address
            vertex_info = vertex_info + "\n" + separator
            vertex_list.append(vertex_info)

        for info in vertex_list:
            print(info)