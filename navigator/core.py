import collections
from navigator import dijkstra, maps, utils

def find_route(start, end):
    """Finds the best route given two coordinate points."""

    lat = float(start.latitude)
    lon = float(start.longitude)
    chunk = maps.download(lat - 0.025, lon - 0.025, lat + 0.025, lon + 0.025)

    node_counter = collections.defaultdict(list)

    for way in chunk.all_ways(roads_only=True):
        for node_id in way.node_ids:
            node_counter[node_id].append(way)

    nodes = {k: dijkstra.Node(k, name=" & ".join([w.tags.get("name", w.tags.get("highway")) for w in v]), data=chunk.get_node(k)) for k, v in node_counter.items() if len(v) > 1}

    def find_closest(lat, lon):
        closest_nodes = {}

        for node in nodes.values():
            if not node.data:
                continue

            closest_nodes[node.id] = utils.haversine(
                float(node.data.lon),
                float(node.data.lat),
                float(lon),
                float(lat)
            )

        return min(closest_nodes, key=closest_nodes.get)

    start = find_closest(start.latitude, start.longitude)
    end = find_closest(end.latitude, end.longitude)

    def calculate_next(node, related_nodes, name):
        distance = 0

        for idx, nd in enumerate(related_nodes):
            current = chunk.get_node(nd)

            try:
                next = chunk.get_node(related_nodes[idx+1])
            except IndexError:
                next = None

            if not next:
                nodes[current.id] = dijkstra.Node(current.id)
                edge = dijkstra.Edge(distance, nodes[current.id], name=name)
                node.edges.append(edge)
                return

            distance += utils.haversine(
                float(current.lon),
                float(current.lat),
                float(next.lon),
                float(next.lat)
            )

            if next.id in nodes:
                edge = dijkstra.Edge(distance, nodes[next.id], name=name)
                node.edges.append(edge)
                return

    for node in nodes.copy().values():
        if not chunk.get_node(node.id):
            continue

        connections = node_counter[node.id]

        for connection in connections:
            i = connection.node_ids.index(node.id)

            if i > 0 and connection.tags.get("oneway") != "yes":
                calculate_next(node, list(reversed(connection.node_ids[:i+1])), connection.tags.get("name"))
            if i + 1 < len(connection.node_ids) and connection.tags.get("oneway") != "-1":
                calculate_next(node, connection.node_ids[i:], connection.tags.get("name"))

    start = nodes[start]
    end = nodes[end]
    r = start.find(end)
    return r
