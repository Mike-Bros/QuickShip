import copy
import itertools

import pandas as pd

from models.Graph import Graph
from models.Graph import Vertex
from services.PlaceService import PlaceService


class DistanceService:
    """A service class to assist with retrieving distance values

    """

    def __init__(self):
        self.distance_list = []
        self.graph = Graph
        self.vertices_added = []
        self.place_list = PlaceService().place_list
        self.ingest_distances()

    def ingest_distances(self):
        """A function that runs during class init to read in Distance data from distances.csv in root.

        """
        print("Ingesting Distances...")
        df = pd.read_csv('./distances.csv', keep_default_na="")
        for index, row in df.iterrows():
            curr_address_distances = []
            for place in self.place_list:
                curr_address_distances.append(row[place.address])
            self.distance_list.append(curr_address_distances)
        print("Finished ingesting Distances")

    def get_place_by_address(self, address):
        for place in self.place_list:
            if place.address == address:
                return place
        return None

    def get_distance_between(self, address_a, address_b):
        """Get Distance Between Addresses

        Given address a & b returns the distance in miles as a float.

        :param address_a:
        :type address_a: str
        :param address_b:
        :type address_b: str
        :return: The distance between address a & b
        :rtype: float
        """
        place_a_index = None
        place_b_index = None

        for place in self.place_list:
            if address_a == place.address:
                place_a_index = place.id - 1
                break

        for place in self.place_list:
            if address_b == place.address:
                place_b_index = place.id - 1
                break

        if place_a_index is None:
            raise Exception('Given address A is unknown')

        if place_b_index is None:
            raise Exception('Given address B is unknown')

        distance_value = self.distance_list[place_a_index][place_b_index]
        if distance_value == '':
            distance_value = self.distance_list[place_b_index][place_a_index]

        return float(distance_value)

    def get_total_distance(self, package_list):
        last_package_address = None
        distance_list = []

        for package in package_list:
            if last_package_address is None:
                last_package_address = copy.deepcopy(package.address)
            else:
                distance_list.append(self.get_distance_between(package.address, last_package_address))

        return sum(distance_list)

    def brute_shortest_path(self, package_list):
        current_cost = float('inf')
        current_best_path = []

        current_best_path_first_half = []
        package_list_first_half = []
        current_best_path_second_half = []
        package_list_second_half = []

        if len(package_list) >= 9:
            count = 0
            for package in package_list:
                count = count + 1
                if count <= 8:
                    package_list_first_half.append(package)
                else:
                    package_list_second_half.append(package)
            count = 0
            for package_list_iteration in itertools.permutations(package_list_first_half):
                count = count + 1
                # print("first half" + str(count))
                iteration_cost = self.get_total_distance(package_list_iteration)
                if iteration_cost < current_cost:
                    current_best_path_first_half = package_list_iteration
                    current_cost = iteration_cost

            count = 0
            current_cost = float('inf')
            for package_list_iteration in itertools.permutations(package_list_second_half):
                count = count + 1
                # print("second half" + str(count))
                iteration_cost = self.get_total_distance(package_list_iteration)
                if iteration_cost < current_cost:
                    current_best_path_second_half = package_list_iteration
                    current_cost = iteration_cost

            for package in current_best_path_first_half:
                current_best_path.append(package)

            for package in current_best_path_second_half:
                current_best_path.append(package)

        else:
            count = 0
            for package_list_iteration in itertools.permutations(package_list):
                count = count + 1
                # print(count)
                iteration_cost = self.get_total_distance(package_list_iteration)
                if iteration_cost < current_cost:
                    current_best_path = package_list_iteration
                    current_cost = iteration_cost

                # print("[", end='')
                # count = 0
                # for package in package_list_iteration:
                #     count = count + 1
                #     if count == len(package_list_iteration):
                #         print(str(package.id) + "] - Itter Cost: " + str(iteration_cost))
                #     else:
                #         print(package.id, end=', ')

        return current_best_path

    # def tsp_shortest_path(self, truck):
    #     route = truck.packages
    #     i =



    # def tsp_shortest_path(self, truck):
    #     # Update services graph attribute with the specified truck argument
    #     self.update_graph(truck)
    #
    #     # Get a copy of the vertices on the graph,
    #     # this will be used to remove vertices as they are visited without interfering with the Graph
    #     unvisited_vertices = list(copy.copy(self.graph.get_vertices()))
    #
    #     smallest_index = 0
    #     while len(unvisited_vertices) > 1:
    #         for i in range(1, len(unvisited_vertices)-1):
    #             print(str(unvisited_vertices[i].label) + " < " + str(unvisited_vertices[smallest_index].label))
    #             print(str(unvisited_vertices[i].distance) + " < " + str(unvisited_vertices[smallest_index].distance))
    #             if unvisited_vertices[i].distance < unvisited_vertices[smallest_index].distance:
    #                 smallest_index = i
    #         current_vertex = unvisited_vertices.pop(smallest_index)
    #
    #         # Check potential path lengths from the current vertex to all vertices
    #         print("Checking potential path lengths for: " + str(current_vertex.label))
    #         for vertex in self.graph.vertices_added[current_vertex]:
    #             edge_weight = self.graph.edge_weights[(current_vertex, vertex)]
    #             print(str(current_vertex.label) + " <-> " + str(vertex.label) + " = " + str(edge_weight))
    #             alternative_path_distance = current_vertex.distance + edge_weight
    #             print("Alternative Path Weight: " + str(alternative_path_distance) + " |" + str(vertex.distance))
    #
    #
    #             # If shorter path from current_vertex to vertex is found, update vertex's distance and predecessor
    #             if alternative_path_distance < vertex.distance:
    #                 vertex.distance = alternative_path_distance
    #                 vertex.previous_vertex = current_vertex
    #
    #     unvisited_vertices = list(copy.copy(self.graph.get_vertices()))
    #     start_vertex = unvisited_vertices.pop(0)
    #     current_best_weight = float('inf')
    #
    #     self.get_path(start_vertex, unvisited_vertices[7])



    def get_path(self, start_vertex, end_vertex):
        path = ""
        current_vertex = end_vertex
        while current_vertex is not start_vertex:
            print("adding current vertex")
            path = " -> " + str(current_vertex.label) + path
            # path.append(current_vertex.label)
            current_vertex = current_vertex.previous_vertex
        print(path)
        return path

    def update_graph(self, truck):
        # Reset graph in case the service has already been used
        self.graph = Graph()

        # Add vertex for starting position
        hub_vert = Vertex(truck.starting_address, truck.starting_address)
        hub_vert.distance = 0
        self.graph.add_vertex(hub_vert)

        # Add all vertices from package_list
        for package in truck.packages:
            vertex_is_unique = True
            new_vertex = Vertex(package.id, package.address)
            for vertex in self.graph.vertices_added:
                if vertex.address == new_vertex.address:
                    vertex_is_unique = False
            if vertex_is_unique:
                self.graph.add_vertex(new_vertex)

        # For each vertex add undirected edge to every other vertex in the graph
        for vertex_a in self.graph.vertices_added:
            # print("Adding undirected edges to all locations from: " + str(vertex_a.address))
            for vertex_b in self.graph.vertices_added:
                a_to_b_weight = self.get_distance_between(vertex_a.address, vertex_b.address)
                # print(str(vertex_a.address) + " <-> " + str(vertex_b.address) + " | Weight = " + str(a_to_b_weight))
                self.graph.add_undirected_edge(vertex_a, vertex_b, a_to_b_weight)
