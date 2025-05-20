````markdown
# Graph Navigator

**Proyecto de navegación de grafos en Python**  
Implementa un sistema interactivo para crear nodos geográficos, conectar aristas con distancias reales, y calcular la ruta más corta entre dos puntos usando el algoritmo de Dijkstra. Está organizado bajo la arquitectura Modelo–Vista–Controlador (MVC) y cuenta con una interfaz de escritorio en Tkinter.

---

## Descripción

Este proyecto permite:  
- Gestionar (CRUD) **nodos** con nombre, latitud y longitud.  
- Definir manualmente **aristas** entre nodos con peso (distancia Haversine).  
- Calcular rutas más cortas entre dos nodos usando una implementación “a mano” de **Dijkstra**.  
- Visualizar el grafo completo y resaltar la ruta encontrada.  
- Interactuar a través de una **aplicación de escritorio** en Python (Tkinter + Matplotlib).

---

## Características principales

| Requisito del PDF                                | Estado                      |
|--------------------------------------------------|-----------------------------|
| CRUD completo de nodos                           | ✔️  `model.py`              |
| Nodo con nombre, latitud y longitud              | ✔️  `model.py`              |
| Conexión de grafos manual (2–3 vecinos por nodo) | ✔️  `main.py` + `haversine` |
| Algoritmo de Dijkstra implementado “a mano”      | ✔️  `model.py`              |
| Interfaz gráfica de escritorio (Tkinter)         | ✔️  `view.py`               |
| Arquitectura MVC en archivos separados           | ✔️  `model.py` / `view.py` / `controller.py` / `main.py` |
| Documentación y manual de usuario                | ✔️  Este README.md         |

---

## Requisitos

- Python 3.8 o superior  
- Paquetes Python:
  ```bash
  pip install matplotlib
````

* Tkinter (incluido normalmente en instalaciones estándar de Python)

---

## Instalación

1. Clona o descarga este repositorio:

   ```bash
   git clone https://tu-repo-url.git
   cd nombre-del-proyecto
   ```
2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```
3. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

   > Si no tienes `requirements.txt`, basta con `pip install matplotlib`.

---

## Estructura del proyecto

```
Proyecto_Final/
├── controller.py      # Lógica de control (eventos, conexión modelo–vista)
├── model.py           # Definición de Node y Graph + Dijkstra “a mano”
├── view.py            # Interfaz Tkinter y canvas Matplotlib
├── main.py            # Punto de entrada + precarga de nodos/aristas
├── requirements.txt   # (opcional) matplotlib
└── README.md          # Documentación y manual
```

---

## Uso

Desde la raíz del proyecto, ejecuta:

```bash
python main.py
```

Se abrirá una ventana con **dos paneles**:

* **Panel izquierdo**: controles para nodos, aristas y cálculo de ruta.
* **Panel derecho**: visualización gráfica del grafo.

---

## Manual de usuario

### 1. Gestión de Nodos

* **Name**: nombre identificador del nodo (ej. “A”).
* **Lat** y **Lon**: coordenadas decimales.
* Botones:

  * **Agregar**: crea un nuevo nodo.
  * **Modificar**: actualiza lat/lon del nodo.
  * **Eliminar**: borra el nodo.
* **Listado**: muestra todos los nodos existentes.

### 2. Gestión de Aristas

* **Desde** / **Hasta**: nodos origen y destino.
* **Distancia**: peso manual (km).
* Botón **Conectar**: crea una arista no dirigida entre ambos nodos.
* **Listado**: muestra todas las conexiones y sus distancias.

### 3. Ruta más corta

* **Inicio** / **Fin**: nodos entre los que quieres calcular la ruta.
* Botón **Calcular**: ejecuta Dijkstra y muestra:

  * **Ruta**: secuencia de nodos.
  * **Dist**: distancia total (km).

### 4. Visualización del Grafo

* **Aristas** en gris.
* **Ruta encontrada** en naranja (más gruesa).
* **Nodos** de la ruta en rojo.
* El panel se ajusta al tamaño de la ventana.

---

## Módulos y responsabilidades

* **model.py**:

  * Clase `Node(name, lat, lon)`
  * Clase `Graph` con métodos CRUD, `_dijkstra()` y `shortest_path()`.
* **view\.py**:

  * Clase `GraphView(tk.Tk)` con widgets y canvas Matplotlib.
  * Métodos: `set_node_list()`, `set_edge_list()`, `set_comboboxes()`, `show_path()`, `draw_graph()`.
* **controller.py**:

  * Clase `GraphController` que enlaza eventos de la vista con la lógica del modelo.
  * Función `haversine()`.
* **main.py**:

  * Precarga de 10 nodos y conexiones (grado 2–3).
  * Inicializa `Graph`, `GraphView` y `GraphController`.

---

## Empaquetado (opcional)

Para generar un ejecutable Windows:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

El `.exe` resultante no requerirá instalación de dependencias.

---

## Mejoras futuras

* **Conectividad garantizada**: integrar un algoritmo MST para asegurar todos los nodos conectados.
* **Guardar/Cargar**: permitir importar y exportar grafos (JSON/CSV).
* **Interfaz web**: migrar UI a Flask, Dash o Streamlit.
* **Estadísticas**: mostrar tiempo de ejecución de Dijkstra y métricas de grafo.

---

```
```
