import collections
import heapdict

class Node:
    def __init__(self, id, *, name=None, data=None, edges=None):
        self.id = id
        self.name = name
        self.data = data
        self.edges = edges or []

    def __str__(self):
        return f"Node {self.id}"

    def __repr__(self):
        return f"<Node {self.id} name={self.name} with {len(self.edges)} edges>"

    def __eq__(self, other):
        return self.id == other.id

    def find(self, destination):
        visited = []
        options = heapdict.heapdict({self.id: SearchNode(self, 0, None)})

        while options:
            current_option = options.popitem()[1]

            if current_option.node == destination:
                break

            for edge in current_option.node.edges:
                distance = current_option.distance + edge.weight

                if edge.node.id in options:
                    conflict_option = options[edge.node.id]

                    if distance < conflict_option.distance:
                        options[edge.node.id] = SearchNode(edge.node, distance, current_option)
                elif edge.node not in visited:
                    options[edge.node.id] = SearchNode(edge.node, distance, current_option)
                    visited.append(edge.node)

        if current_option.node != destination:
            raise NoRouteError(self, destination)

        route = []
        disatnce = current_option.distance

        while True:
            route.append(current_option.node)

            if current_option.node == self:
                break

            current_option = current_option.previous

        return (list(reversed(route)), distance)

class Edge:
    def __init__(self, weight, node, *, name=None, data=None):
        self.weight = weight
        self.node = node
        self.name = name
        self.data = data

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Edge {self.name} weight={self.weight}>"

class NoRouteError(Exception):
    def __init__(self, start, end):
        super().__init__(f"{start} aqnd {end} are not connected to each other")

class SearchNode:
    def __init__(self, node, distance, previous):
        self.node = node
        self.distance = distance
        self.previous = previous

    def __eq__(self, other):
        return self.distance == other.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __gt__(self, other):
        return self.distance > other.distance
 