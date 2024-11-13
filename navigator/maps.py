import geocoder
import requests

from lxml import etree

class Location:
    """Represents a real-life location such as a house, school, park, or workplace on a map."""

    def __init__(self, data):
        self._data = data
        self.latitude = data["lat"]
        self.longitude = data["lon"]
        self.display_name = data["display_name"]

    def __str__(self):
        return self.display_name

    @classmethod
    def from_coords(self, lat, lon):
        return cls({
            "lat": lat,
            "lon": lon,
            "display_name": None
        })

class Map:
    """Represents a section of OSM map."""

    def __init__(self, content):
        self._tree = etree.fromstring(content)
        self._nodes = {node.attrib["id"]: Node(node) for node in self._tree.xpath("node")}
        self._ways = [Way(way) for way in self._tree.xpath("way")]

    def get_node(self, node_id):
        """Returns a node based on the ID."""

        return self._nodes.get(node_id)

    def get_way(self, way_id):
        """Returns a way based on the ID."""

        return self._ways.get(way_id)

    def all_nodes(self):
        """Returns a list of all nodes on the map."""

        return list(self._nodes.values())

    def all_ways(self, roads_only=False):
        """Returns a list of all ways on the map."""

        if roads_only:
            ignored = ("pedestrian", "footway", "cycleway", "bridleway", None)
        else:
            ignored = ()

        return [way for way in self._ways if way.tags.get("highway") not in ignored]

    def to_graph(self):
        """
        Returns a weighted directed graph with edges representing the roads and the nodes representing the intersections or ends.

        Weights are distances in kilometers.
        """

        node_counter = collections.defaultdict(list)

        for way in chunk.all_ways(roads_only=True):
            for node_id in way.node_ids:
                node_counter[node_id].append(way)

        nodes = {k: dijkstra.Node(k, name=" & ".join([w.tags.get("name", w.tags.get("highway")) for w in v])) for k, v in node_counter.items() if len(v) > 1}

        return nodes

class Node:
    """Represents a coordinate point on a map."""

    def __init__(self, element):
        self._element = element

        self.id = element.attrib["id"]
        self.lat = element.attrib["lat"]
        self.lon = element.attrib["lon"]

class Way:
    """Represents a way on a map."""

    def __init__(self, element):
        self._element = element

        self.id = element.attrib["id"]
        self.node_ids = [nd.attrib["ref"] for nd in element.xpath("nd")]
        self.tags = {tag.attrib["k"]: tag.attrib["v"] for tag in element.xpath("tag")}

def search_location(query):
    """Returns a location based on the provided serach query."""

    params = {"q": query, "format": "json"}
    resp = requests.get(f"https://nominatim.openstreetmap.org/search", params=params)
    return Location(resp.json()[0])

def get_current_coordinates(self):
    return geocoder.ip("me").latlng

def download(lat1, lon1, lat2, lon2):
    """Downloads a section of OSM map."""

    resp = requests.get(f"http://overpass-api.de/api/interpreter?data=[out:xml];(node({lat1},{lon1},{lat2},{lon2});<;);out meta;")
    return Map(resp.content)
    
    return etree.fromstring(resp.content)
