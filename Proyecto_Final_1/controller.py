import random, math
from tkinter import messagebox
from model import Graph

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    φ1,φ2 = math.radians(lat1), math.radians(lat2)
    dφ = math.radians(lat2-lat1)
    dλ = math.radians(lon2-lon1)
    a = math.sin(dφ/2)**2 + math.cos(φ1)*math.cos(φ2)*math.sin(dλ/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1-a))

class GraphController:
    def __init__(self, model: Graph, view):
        self.g = model
        self.v = view
        self._connect()
        self._refresh()

    def _connect(self):
        self.v.btn_add_node .config(command=self.on_add_node)
        self.v.btn_upd_node .config(command=self.on_upd_node)
        self.v.btn_del_node .config(command=self.on_del_node)
        self.v.btn_add_edge .config(command=self.on_add_edge)
        self.v.btn_path     .config(command=self.on_compute_path)

    def _refresh(self):
        nodes = self.g.list_nodes()
        self.v.set_node_list(nodes)
        self.v.set_comboboxes(nodes)
        self.v.set_edge_list(self.g.list_edges())
        self.v.draw_graph(self.g.nodes, self.g.adj)

    # --- NODES ---
    def on_add_node(self):
        try:
            name = self.v.name_in.get()
            lat  = float(self.v.lat_in.get())
            lon  = float(self.v.lon_in.get())
            self.g.add_node(name, lat, lon)
        except Exception as e:
            messagebox.showerror("Error al añadir nodo", str(e))
        self._refresh()

    def on_upd_node(self):
        try:
            name = self.v.name_in.get()
            lat  = float(self.v.lat_in.get())
            lon  = float(self.v.lon_in.get())
            self.g.update_node(name, lat, lon)
        except Exception as e:
            messagebox.showerror("Error al modificar nodo", str(e))
        self._refresh()

    def on_del_node(self):
        try:
            name = self.v.name_in.get()
            self.g.delete_node(name)
        except Exception as e:
            messagebox.showerror("Error al eliminar nodo", str(e))
        self._refresh()

    # --- EDGES ---
    def on_add_edge(self):
        try:
            u = self.v.edge_u.get()
            v = self.v.edge_v.get()
            d = float(self.v.edge_d.get())
            self.g.add_edge(u, v, d)
        except Exception as e:
            messagebox.showerror("Error al conectar", str(e))
        self._refresh()

    # --- DIJKSTRA ---
    def on_compute_path(self):
        try:
            start = self.v.start_cb.get()
            end   = self.v.end_cb.get()
            path, dist = self.g.shortest_path(start, end)
        except Exception as e:
            messagebox.showerror("Error ruta", str(e))
            path, dist = None, None
        self.v.show_path(path, dist)
        self._refresh()
