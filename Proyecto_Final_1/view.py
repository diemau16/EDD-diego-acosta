import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GraphView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Navigator")
        self.geometry("1000x700")
        self.current_path = []

        # Contenedor principal
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)

        # Panel izquierdo: controles
        controls = ttk.Frame(main)
        controls.pack(side="left", fill="y", padx=5, pady=5)

        # Panel derecho: gráfica
        graph_frame = ttk.LabelFrame(main, text="Visualización del Grafo")
        graph_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # --- Nodos ---
        node_frame = ttk.LabelFrame(controls, text="Nodos")
        node_frame.pack(fill="x", pady=5)
        ttk.Label(node_frame, text="Name").grid(row=0, column=0, sticky="w")
        self.name_in = ttk.Entry(node_frame); self.name_in.grid(row=0, column=1, sticky="we")
        ttk.Label(node_frame, text="Lat").grid(row=1, column=0, sticky="w")
        self.lat_in = ttk.Entry(node_frame);  self.lat_in.grid(row=1, column=1, sticky="we")
        ttk.Label(node_frame, text="Lon").grid(row=2, column=0, sticky="w")
        self.lon_in = ttk.Entry(node_frame);  self.lon_in.grid(row=2, column=1, sticky="we")
        self.btn_add_node = ttk.Button(node_frame, text="Agregar");   self.btn_add_node.grid(row=0, column=2, padx=5)
        self.btn_upd_node = ttk.Button(node_frame, text="Modificar"); self.btn_upd_node.grid(row=1, column=2, padx=5)
        self.btn_del_node = ttk.Button(node_frame, text="Eliminar");  self.btn_del_node.grid(row=2, column=2, padx=5)
        self.lst_nodes = tk.Listbox(node_frame, height=4)
        self.lst_nodes.grid(row=3, column=0, columnspan=3, sticky="we", pady=5)

        # --- Aristas ---
        edge_frame = ttk.LabelFrame(controls, text="Aristas")
        edge_frame.pack(fill="x", pady=5)
        ttk.Label(edge_frame, text="Desde").grid(row=0, column=0, sticky="w")
        self.edge_u = ttk.Combobox(edge_frame, values=[]); self.edge_u.grid(row=0, column=1, sticky="we")
        ttk.Label(edge_frame, text="Hasta").grid(row=1, column=0, sticky="w")
        self.edge_v = ttk.Combobox(edge_frame, values=[]); self.edge_v.grid(row=1, column=1, sticky="we")
        ttk.Label(edge_frame, text="Distancia").grid(row=2, column=0, sticky="w")
        self.edge_d = ttk.Entry(edge_frame); self.edge_d.grid(row=2, column=1, sticky="we")
        self.btn_add_edge = ttk.Button(edge_frame, text="Conectar"); self.btn_add_edge.grid(row=0, column=2, padx=5)
        self.lst_edges = tk.Listbox(edge_frame, height=4)
        self.lst_edges.grid(row=3, column=0, columnspan=3, sticky="we", pady=5)

        # --- Puntos intermedios ---
        inter_frame = ttk.LabelFrame(controls, text="Puntos intermedios\n(Ctrl+clic para varios)")
        inter_frame.pack(fill="x", pady=5)
        self.inter_list = tk.Listbox(inter_frame, selectmode="multiple", height=4)
        self.inter_list.pack(fill="both", expand=True)

        # --- Ruta más corta ---
        path_frame = ttk.LabelFrame(controls, text="Ruta más corta")
        path_frame.pack(fill="x", pady=5)
        ttk.Label(path_frame, text="Inicio").grid(row=0, column=0, sticky="w")
        self.start_cb = ttk.Combobox(path_frame, values=[]); self.start_cb.grid(row=0, column=1, sticky="we")
        ttk.Label(path_frame, text="Fin").grid(row=1, column=0, sticky="w")
        self.end_cb   = ttk.Combobox(path_frame, values=[]); self.end_cb.grid(row=1, column=1, sticky="we")
        self.btn_path = ttk.Button(path_frame, text="Calcular"); self.btn_path.grid(row=0, column=2, rowspan=2, padx=5)
        self.lbl_path = ttk.Label(path_frame, text="Ruta: —\nDist: — km"); self.lbl_path.grid(row=2, column=0, columnspan=3, pady=5)

        # --- Canvas Matplotlib ---
        self.fig = Figure(figsize=(6,5))
        self.ax  = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # Métodos esperados por el controlador
    def set_node_list(self, nodes):
        self.lst_nodes.delete(0, tk.END)
        for n in nodes:
            self.lst_nodes.insert(tk.END, n)

    def set_edge_list(self, edges):
        self.lst_edges.delete(0, tk.END)
        for u, nbrs in edges.items():
            line = ", ".join(f"{v}({d:.1f})" for v, d in nbrs.items())
            self.lst_edges.insert(tk.END, f"{u} → {line}")

    def set_comboboxes(self, nodes):
        for cb in (self.edge_u, self.edge_v, self.start_cb, self.end_cb):
            cb['values'] = nodes

    def set_inter_list(self, nodes):
        self.inter_list.delete(0, tk.END)
        for n in nodes:
            self.inter_list.insert(tk.END, n)

    def show_path(self, path, dist):
        if path is None:
            self.lbl_path.config(text="Ruta: —\nDist: no existe")
            self.current_path = []
        else:
            self.lbl_path.config(text=f"Ruta: {' → '.join(path)}\nDist: {dist:.2f} km")
            self.current_path = path

    def draw_graph(self, nodes, adj):
        self.ax.clear()
        seen = set()
        # dibujar aristas
        for u, nbrs in adj.items():
            for v, d in nbrs.items():
                if (v,u) in seen: continue
                seen.add((u,v))
                x0,y0 = nodes[u].lon, nodes[u].lat
                x1,y1 = nodes[v].lon, nodes[v].lat
                self.ax.plot([x0,x1],[y0,y1], color='gray', linewidth=1)
        # dibujar nodos
        for n, nd in nodes.items():
            color = 'red' if n in self.current_path else 'black'
            self.ax.scatter(nd.lon, nd.lat, color=color)
            self.ax.text(nd.lon, nd.lat, n, color=color)
        # resaltar ruta
        if self.current_path and len(self.current_path) > 1:
            for i in range(len(self.current_path)-1):
                u,v = self.current_path[i], self.current_path[i+1]
                x0,y0 = nodes[u].lon, nodes[u].lat
                x1,y1 = nodes[v].lon, nodes[v].lat
                self.ax.plot([x0,x1],[y0,y1], color='orange', linewidth=2.5)
        self.ax.set_xlabel("Longitud")
        self.ax.set_ylabel("Latitud")
        self.canvas.draw()
