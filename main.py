# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice
import random

DAY_NAMES = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

# Lista de rutas base
rutas = [
    ("Portal Norte", "Pepe Sierra", 8, [0, 1, 2, 3, 4, 5]),
    ("Pepe Sierra", "Calle 100", 6, [0, 1, 2, 3, 4, 5]),
    ("Calle 100", "Av. 72", 5, [0, 1, 2, 3, 4, 5, 6]),
    ("Av. 72", "Av. Chile", 4, [0, 1, 2, 3, 4]),
    ("Av. Chile", "Calle 45", 4, [0, 1, 2, 3, 4, 5]),
    ("Calle 45", "Av. Jimenez", 6, [0, 1, 2, 3, 4, 5, 6]),
    ("Av. Jimenez", "Zona Industrial", 7, [0, 1, 2, 3, 4, 5]),
    ("Zona Industrial", "Banderas", 9, [0, 1, 2, 3, 4, 5]),
    ("Banderas", "Portal Americas", 6, [0, 1, 2, 3, 4, 5, 6]),
    ("Portal Norte", "Calle 170", 3, [0, 1, 2, 3, 4, 5, 6]),
    ("Calle 170", "Calle 146", 4, [0, 1, 2, 3, 4, 5]),
    ("Calle 146", "Calle 142", 3, [0, 1, 2, 3, 4, 5]),
    ("Calle 142", "Pepe Sierra", 5, [0, 1, 2, 3, 4, 5]),
    ("Av. Jimenez", "Av. 26", 3, [0, 1, 2, 3, 4, 5, 6]),
    ("Av. 26", "Zona Industrial", 4, [0, 1, 2, 3, 4, 5, 6]),
    ("Zona Industrial", "Av. 68", 5, [0, 1, 2, 3, 4, 5]),
    ("Av. 68", "Banderas", 5, [0, 1, 2, 3, 4, 5]),
    ("Calle 100", "Av. 85", 4, [0, 1, 2, 3, 4, 5, 6]),
    ("Av. 85", "Av. Chile", 3, [0, 1, 2, 3, 4, 5]),
    ("Av. Jimenez", "Av. 63", 6, [0, 1, 2, 3, 4, 5, 6]),
    ("Av. 63", "Zona Industrial", 5, [0, 1, 2, 3, 4, 5]),
]

# Coordenadas
coordenadas = {
    "Portal Norte": (-74.0479, 4.7655),
    "Calle 170": (-74.0460, 4.7426),
    "Calle 146": (-74.0462, 4.7330),
    "Calle 142": (-74.0465, 4.7300),
    "Pepe Sierra": (-74.0472, 4.7254),
    "Calle 100": (-74.0511, 4.6818),
    "Av. 85": (-74.0584, 4.6722),
    "Av. 72": (-74.0615, 4.6599),
    "Av. Chile": (-74.0645, 4.6540),
    "Calle 45": (-74.0702, 4.6425),
    "Av. 26": (-74.0911, 4.6421),
    "Av. Jimenez": (-74.0733, 4.6097),
    "Zona Industrial": (-74.0958, 4.6291),
    "Av. 63": (-74.0667, 4.6489),
    "Av. 68": (-74.1114, 4.6413),
    "Banderas": (-74.1287, 4.6214),
    "Portal Americas": (-74.1572, 4.6167),
}


# Crear grafo con tr‡fico aleatorio
def crear_grafo(dia):
    G = nx.DiGraph()
    for u, v, tiempo, dias in rutas:
        if dia in dias:
            # Simulamos tr‡fico con +/- 30% variaci—n
            factor = random.uniform(0.7, 1.3)
            G.add_edge(u, v, weight=tiempo * factor)
    return G


# Encontrar k rutas
def encontrar_k_rutas(G, origen, destino, k=3):
    try:
        rutas = list(
            islice(nx.shortest_simple_paths(G, origen, destino, weight="weight"), k)
        )
        tiempos = []
        for ruta in rutas:
            tiempo = sum(G[u][v]["weight"] for u, v in zip(ruta[:-1], ruta[1:]))
            tiempos.append((ruta, round(tiempo, 1)))
        return tiempos
    except nx.NetworkXNoPath:
        return []


# Visualizaci—n
def visualizar_rutas(G, rutas, coordenadas):
    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos=coordenadas,
        node_size=200,
        with_labels=True,
        alpha=0.6,
        font_size=8,
        edge_color="lightgray",
    )
    colores = ["yellow", "blue", "red"]
    for i, (path, tiempo) in enumerate(
        rutas[::-1]
    ):  # invertimos para que rojo quede arriba
        edges_in_path = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            G,
            pos=coordenadas,
            edgelist=edges_in_path,
            edge_color=colores[i],
            width=3,
            alpha=0.9,
        )
    plt.show()


# -------- MAIN --------
origen = "Portal Norte"
destino = "Portal Americas"

dia_str = (
    input(
        "Dia de la semana (lunes, martes, miercoles, jueves, viernes, sabado, domingo): "
    )
    .strip()
    .lower()
)
if dia_str not in DAY_NAMES:
    print("Dia invalido.")
else:
    dia = DAY_NAMES.index(dia_str)
    G_dia = crear_grafo(dia)

    rutas_encontradas = encontrar_k_rutas(G_dia, origen, destino, k=3)

    if rutas_encontradas:
        print(f"Rutas disponibles el {dia_str} entre {origen} y {destino}:")
        for i, (ruta, tiempo) in enumerate(rutas_encontradas):
            print(f"Ruta {i + 1}: {ruta}, tiempo estimado: {tiempo} minutos")
        visualizar_rutas(G_dia, rutas_encontradas, coordenadas)
    else:
        print(f"No hay rutas disponibles el {dia_str}.")
