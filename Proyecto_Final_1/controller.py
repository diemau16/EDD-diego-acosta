import random
import math
import itertools
from tkinter import messagebox
from model import Graph
from view import GraphView

def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    dφ = math.radians(lat2 - lat1)
    dλ = math.radians(lon2 - lon1)
    a = math.sin(dφ/2)**2 + math.cos(φ1)*math.cos(φ2)*math.sin(dλ/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

class GraphController:
    def __init__(self, graph: Graph, view: GraphView):
        self.g = graph
        self.v = view
        self._connect_handlers()
        self._refresh()

    def _connect_handlers(self):
        # CRUD nodos
        self.v.btn_add_node.config(command=self.on_add_node)
        self.v.btn_upd_node.config(command=self.on_upd_node)
        self.v.btn_del_node.config(command=self.on_del_node)
        # CRUD aristas
        self.v.btn_add_edge.config(command=self.on_add_edge)
        # Ruta con intermedios
        self.v.btn_path.config(command=self.on_compute_path)

    def _refresh(self):
        # Actualiza todas las vistas
        nodes = self.g.list_nodes()
        self.v.set_node_list(nodes)
        self.v.set_comboboxes(nodes)
        self.v.set_inter_list(nodes)
        self.v.set_edge_list(self.g.list_edges())
        self.v.draw_graph(self.g.nodes, self.g.adj)

    # --- Manejadores de nodos ---
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

    # --- Manejador de aristas ---
    def on_add_edge(self):
        try:
            u = self.v.edge_u.get()
            v = self.v.edge_v.get()
            d = float(self.v.edge_d.get())
            self.g.add_edge(u, v, d)
        except Exception as e:
            messagebox.showerror("Error al conectar arista", str(e))
        self._refresh()

    # --- Manejador de ruta con intermedios ---
    def on_compute_path(self):
        start = self.v.start_cb.get()
        end   = self.v.end_cb.get()
        sel   = self.v.inter_list.curselection()
        mids  = [self.v.inter_list.get(i) for i in sel]

        best_path, best_dist = None, math.inf

        # Probar todas las permutaciones de puntos intermedios
        for perm in itertools.permutations(mids):
            seq = [start] + list(perm) + [end]
            total = 0
            segments = []
            valid = True
            for i in range(len(seq) - 1):
                seg, dist = self.g.shortest_path(seq[i], seq[i+1])
                if seg is None:
                    valid = False
                    break
                segments.append((seg, dist))
                total += dist
            if valid and total < best_dist:
                best_dist = total
                best_path = segments

        if best_path is None:
            messagebox.showwarning("Ruta", "No existe ruta que conecte esos puntos.")
            self.v.show_path(None, 0)
        else:
            # Reconstruir ruta completa sin repetir nodos
            full = []
            for idx, (seg, _) in enumerate(best_path):
                if idx == 0:
                    full.extend(seg)
                else:
                    full.extend(seg[1:])
            self.v.show_path(full, best_dist)

        self._refresh()
