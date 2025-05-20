import math
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Node:
    name: str
    lat: float
    lon: float

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adj:   Dict[str, Dict[str, float]] = {}

    # ---- CRUD NODES ----
    def add_node(self, name: str, lat: float, lon: float):
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists.")
        self.nodes[name] = Node(name, lat, lon)
        self.adj[name] = {}

    def update_node(self, name: str, lat: float, lon: float):
        if name not in self.nodes:
            raise KeyError(f"Node '{name}' not found.")
        self.nodes[name].lat = lat
        self.nodes[name].lon = lon

    def delete_node(self, name: str):
        if name not in self.nodes:
            raise KeyError(f"Node '{name}' not found.")
        del self.nodes[name]
        del self.adj[name]
        for nbrs in self.adj.values():
            nbrs.pop(name, None)

    def list_nodes(self) -> List[str]:
        return list(self.nodes.keys())

    # ---- CRUD EDGES ----
    def add_edge(self, u: str, v: str, dist: float):
        if u not in self.nodes or v not in self.nodes:
            raise KeyError("Both nodes must exist.")
        self.adj[u][v] = dist
        self.adj[v][u] = dist

    def list_edges(self) -> Dict[str, Dict[str, float]]:
        return self.adj

    # ---- DIJKSTRA ----
    def _dijkstra(self, start: str):
        dist = {n: math.inf for n in self.nodes}
        prev = {n: None      for n in self.nodes}
        dist[start] = 0.0
        unvis = set(self.nodes)
        while unvis:
            u = min(unvis, key=lambda x: dist[x])
            unvis.remove(u)
            for v, w in self.adj[u].items():
                if v in unvis and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
        return dist, prev

    def shortest_path(self, start: str, end: str) -> (Optional[List[str]], float):
        if start not in self.nodes or end not in self.nodes:
            raise KeyError("Start or end node not found.")
        dist, prev = self._dijkstra(start)
        if dist[end] == math.inf:
            return None, math.inf
        path = []
        u = end
        while u:
            path.insert(0, u)
            u = prev[u]
        return path, dist[end]
