import heapq
import math

def dijkstra(nodos, aristas, origen, destino, dirigido=False, bloqueados=()):
    nodos = set(nodos)
    bloqueados = set(bloqueados)
    if origen not in nodos or destino not in nodos or not bloqueados <= nodos:
        raise ValueError("Nodo desconocido")
    adj = {v: [] for v in nodos}
    for u, v, peso in aristas:
        if u not in nodos or v not in nodos or not isinstance(peso, (int, float)) or not math.isfinite(peso) or peso < 0:
            raise ValueError("Arista invalida")
        if u not in bloqueados and v not in bloqueados:
            adj[u].append((v, peso))
            if not dirigido:
                adj[v].append((u, peso))
    if origen in bloqueados or destino in bloqueados:
        return math.inf, []
    dist = {v: math.inf for v in nodos}
    prev = {}
    dist[origen] = 0
    cola = [(0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if d != dist[u]:
            continue
        if u == destino:
            ruta = [u]
            while ruta[-1] != origen:
                ruta.append(prev[ruta[-1]])
            return d, ruta[::-1]
        for v, peso in adj[u]:
            nuevo = d + peso
            if nuevo < dist[v]:
                dist[v] = nuevo
                prev[v] = u
                heapq.heappush(cola, (nuevo, v))
    return math.inf, []
