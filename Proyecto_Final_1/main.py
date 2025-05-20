# main.py

import random
from model import Graph
from view import GraphView
from controller import GraphController, haversine

def preload(graph: Graph):
    # 1) Definir 10 nodos de ejemplo
    initial = [
        ("A",  0.0,  0.0),
        ("B",  1.0,  2.0),
        ("C",  3.0,  1.0),
        ("D", -1.0,  2.5),
        ("E",  2.0, -2.0),
        ("F", -2.0, -1.0),
        ("G",  4.0,  0.0),
        ("H",  0.0, -3.0),
        ("I",  5.0,  3.0),
        ("J", -3.0, -2.0),
    ]
    for name, lat, lon in initial:
        graph.add_node(name, lat, lon)

    # 2) Determinar grado objetivo (2 o 3) para cada nodo
    degrees = {u: random.choice([2, 3]) for u in graph.list_nodes()}

    # 3) Asegurar que la suma de grados sea par
    if sum(degrees.values()) % 2 != 0:
        # elige un nodo al azar y cambia 2↔3
        n = random.choice(list(degrees.keys()))
        degrees[n] = 5 - degrees[n]

    # 4) Crear la lista de “stubs”
    stubs = []
    for u, deg in degrees.items():
        stubs.extend([u] * deg)
    random.shuffle(stubs)

    # 5) Emparejar stubs para generar aristas
    added = set()  # para evitar duplicados
    while stubs:
        u = stubs.pop()
        # buscar un compañero v válido
        for i, v in enumerate(stubs):
            if v != u and (u, v) not in added and (v, u) not in added:
                # calcular distancia real
                d = haversine(
                    graph.nodes[u].lat, graph.nodes[u].lon,
                    graph.nodes[v].lat, graph.nodes[v].lon
                )
                graph.add_edge(u, v, d)
                added.add((u, v))
                # retirar el stub emparejado
                stubs.pop(i)
                break
        else:
            # si no encontramos compañero, abandonamos ese stub
            # (suele ocurrir muy rara vez en grafos pequeños)
            continue

if __name__ == "__main__":
    g = Graph()
    preload(g)

    view = GraphView()
    ctrl = GraphController(g, view)

    # Para aplicación Tkinter:
    view.mainloop()
