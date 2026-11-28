import heapq
import math

def dijkstra(nodos, aristas, origen, destino, dirigido=False, bloqueados=()):
    """Ruta mínima del AMR en la planta (Dijkstra).

    Entrada: conjunto de nodos, aristas (u, v, peso) con peso finito >= 0,
    origen, destino, si el grafo es dirigido y nodos bloqueados.
    Salida: (costo, ruta). Si no hay ruta devuelve (inf, []).

    Precondición: pesos no negativos; por eso el primer nodo extraído con
    su distancia vigente ya es mínimo y no puede mejorarse después.
    Terminación: cada nodo se asienta una vez y cada arista produce a lo
    sumo una relajación exitosa por extremo; la cola es finita.
    Tiempo O((V + E) log V) con heap binario; espacio O(V + E).
    """
    nodos = set(nodos)
    bloqueados = set(bloqueados)
    if origen not in nodos or destino not in nodos or not bloqueados <= nodos:
        raise ValueError("Nodo desconocido")
    adj = {v: [] for v in nodos}
    for u, v, peso in aristas:
        if u not in nodos or v not in nodos or not isinstance(peso, (int, float)) or not math.isfinite(peso) or peso < 0:
            raise ValueError("Arista invalida")
        # Una zona bloqueada elimina todas sus aristas incidentes.
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
        if d != dist[u]:  # entrada obsoleta de la cola
            continue
        if u == destino:  # destino asentado: reconstruir con predecesores
            ruta = [u]
            while ruta[-1] != origen:
                ruta.append(prev[ruta[-1]])
            return d, ruta[::-1]
        for v, peso in adj[u]:
            nuevo = d + peso
            if nuevo < dist[v]:  # relajación
                dist[v] = nuevo
                prev[v] = u
                heapq.heappush(cola, (nuevo, v))
    return math.inf, []
