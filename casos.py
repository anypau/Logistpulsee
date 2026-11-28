"""Algoritmos y verificadores de los diez correos del simulador LOGISTPULSE.

Convenciones de complejidad:
    V, E  vértices y aristas del grafo;
    n     vértices, centros o variables según el caso;
    m     cláusulas de la fórmula;
    B     cota de búsqueda; b bits del número en binario.

Cada caso NP o NP-completo tiene dos funciones separadas:
    * un **verificador** polinómico, que recibe un certificado y responde
      True/False sin lanzar excepciones ante certificados mal formados;
    * una **búsqueda exacta** (exponencial o pseudo-polinómica), útil solo
      para instancias pequeñas; termina siempre porque el espacio de
      candidatos es finito.
"""

from collections import deque
from heapq import heappop, heappush
from itertools import combinations, permutations
from math import inf


# ---------------------------------------------------------------------------
# Grupo A · P
# ---------------------------------------------------------------------------

def bfs(edges, s, t):
    """P1 · Alcanzabilidad en grafo dirigido.

    Entrada: lista de aristas dirigidas (u, v), origen s y destino t.
    Salida: True si existe un camino de s a t.
    Algoritmo exacto: BFS con cola y conjunto de visitados; cada vértice
    entra a la cola a lo sumo una vez, por lo que termina.
    Tiempo O(V + E); espacio O(V + E) (lista de adyacencia + visitados).
    """
    g = {}
    for u, v in edges:
        g.setdefault(u, []).append(v)
    cola = deque([s])
    visitados = {s}
    while cola:
        u = cola.popleft()
        if u == t:
            return True
        for v in g.get(u, []):
            if v not in visitados:
                visitados.add(v)
                cola.append(v)
    return False


def shortest(edges, s):
    """P2 · Distancias mínimas desde s (Dijkstra).

    Entrada: aristas dirigidas (u, v, w) con w >= 0 y origen s.
    Salida: (dist, prev); dist[v] = inf si v no es alcanzable y prev permite
    reconstruir el camino. Se rechazan pesos negativos porque invalidan la
    propiedad de asentamiento de Dijkstra.
    Algoritmo exacto con heap binario y entradas obsoletas descartadas.
    Tiempo O((V + E) log V); espacio O(V + E).
    """
    g = {s: []}
    for u, v, w in edges:
        if w < 0:
            raise ValueError("Peso negativo")
        g.setdefault(u, []).append((v, w))
        g.setdefault(v, [])
    dist = dict.fromkeys(g, inf)
    dist[s] = 0
    prev = {}
    cola = [(0, s)]
    while cola:
        d, u = heappop(cola)
        if d != dist[u]:          # entrada obsoleta: u ya se asentó antes
            continue
        for v, w in g[u]:
            if d + w < dist[v]:   # relajación
                dist[v] = d + w
                prev[v] = u
                heappush(cola, (dist[v], v))
    return dist, prev


def maxflow(edges, s, t):
    """P3 · Flujo máximo (Edmonds–Karp).

    Entrada: aristas (u, v, c) con capacidad entera c >= 0, fuente s y
    sumidero t distintos. Salida: (flujo_total, registro de caminos
    aumentantes). Cada iteración busca el camino aumentante más corto con
    BFS en la red residual; el teorema flujo máximo/corte mínimo garantiza
    optimalidad al no quedar caminos. Termina tras O(VE) aumentos.
    Tiempo O(V E^2); espacio O(V + E) sin contar el registro.
    """
    if s == t:
        raise ValueError("Origen igual a destino")
    residual = {s: {}, t: {}}
    for u, v, c in edges:
        if type(c) is not int or c < 0:
            raise ValueError("Capacidad invalida")
        residual.setdefault(u, {})
        residual.setdefault(v, {})
        residual[u][v] = residual[u].get(v, 0) + c   # aristas paralelas se suman
        residual[v].setdefault(u, 0)                 # arista inversa residual
    total = 0
    registro = []
    while True:
        padre = {s: None}
        cola = deque([s])
        while cola and t not in padre:
            u = cola.popleft()
            for v, c in residual[u].items():
                if c > 0 and v not in padre:
                    padre[v] = u
                    cola.append(v)
        if t not in padre:
            return total, registro
        camino = [t]
        while camino[-1] != s:
            camino.append(padre[camino[-1]])
        camino.reverse()
        pares = list(zip(camino, camino[1:]))
        cuello = min(residual[u][v] for u, v in pares)
        for u, v in pares:
            residual[u][v] -= cuello
            residual[v][u] += cuello
        total += cuello
        registro.append((camino, cuello))


# ---------------------------------------------------------------------------
# Grupo B · NP (pertenencia mediante certificado)
# ---------------------------------------------------------------------------

def matrix(A):
    """Valida que A sea una matriz de adyacencia cuadrada con entradas 0/1."""
    if any(len(fila) != len(A) or any(x not in (0, 1) for x in fila) for fila in A):
        raise ValueError("Matriz invalida")


def verify_iso(A, B, p):
    """N1 · Verificador de isomorfismo.

    Certificado: permutación p de {0..n-1} (O(n log n) bits).
    Comprueba que p sea biyección y que A[i][j] == B[p(i)][p(j)] para todo
    par. Tiempo O(n^2); espacio auxiliar O(n).
    """
    matrix(A)
    matrix(B)
    n = len(A)
    return (len(B) == n and len(p) == n and set(p) == set(range(n))
            and all(A[i][j] == B[p[i]][p[j]] for i in range(n) for j in range(n)))


def iso(A, B, nontrivial=False):
    """N1/N4 · Búsqueda exacta de isomorfismo por enumeración.

    Prueba las n! permutaciones y devuelve la primera que el verificador
    acepta, o None. Con nontrivial=True se omite la identidad (uso en N4,
    donde B = A). Termina porque hay finitas permutaciones.
    Tiempo O(n! n^2); espacio O(n) auxiliar más las matrices.
    """
    matrix(A)
    matrix(B)
    if len(A) != len(B):
        return None
    identidad = tuple(range(len(A)))
    for p in permutations(range(len(A))):
        if nontrivial and p == identidad:
            continue
        if verify_iso(A, B, p):
            return p
    return None


def verify_auto(A, p):
    """N4 · Verificador de automorfismo no trivial.

    Certificado: permutación p distinta de la identidad que preserva A.
    Tiempo O(n^2); espacio O(n).
    """
    return tuple(p) != tuple(range(len(A))) and verify_iso(A, A, p)


def verify_factor(N, B, d):
    """N2 · Verificador de divisor acotado.

    Certificado: entero d con 2 <= d <= B que divide a N (N >= 2).
    Con división escolar en binario: tiempo O(b^2), espacio O(b).
    """
    return (type(N) is int and N >= 2 and type(B) is int
            and type(d) is int and 2 <= d <= B and N % d == 0)


def factor(N, B):
    """N2 · Búsqueda exacta del menor divisor d en [2, min(B, N)].

    None significa que no hay divisor <= B (no necesariamente que N sea
    primo, salvo que B >= N). Pseudo-polinómico: O(min(B, N) b^2), que es
    exponencial en la longitud binaria b.
    """
    if N < 2 or B < 0:
        raise ValueError("Parametros invalidos")
    return next((d for d in range(2, min(B, N) + 1) if verify_factor(N, B, d)), None)


def verify_log(p, g, h, B, x):
    """N3 · Verificador de logaritmo discreto acotado.

    Certificado: entero 0 <= x <= B con g^x mod p == h. Usa
    exponenciación modular rápida: O(log(B+1) b^2) con b bits de p.
    """
    return (type(p) is int and p >= 2 and type(x) is int and 0 <= x <= B
            and pow(g, x, p) == h)


def discrete(p, g, h, B):
    """N3 · Búsqueda exacta incremental del menor x <= B.

    Precondición del problema: p primo y g, h residuos canónicos (la
    primalidad no se verifica; la búsqueda es correcta igualmente).
    Mantiene v = g^x mod p con una multiplicación por paso.
    Tiempo O((B+1) b^2); espacio O(b + log(B+1)) bits.
    """
    if p < 2 or not 0 <= g < p or not 0 <= h < p or B < 0:
        raise ValueError("Parametros invalidos")
    v = 1 % p
    for x in range(B + 1):
        if v == h:
            return x
        v = v * g % p
    return None


# ---------------------------------------------------------------------------
# Grupo C · NP-completo
# ---------------------------------------------------------------------------

def verify_sat(clauses, n, a):
    """C1 · Verificador de SAT (CNF).

    Certificado: asignación a = {1..n -> bool}. Cada literal l > 0 es x_l y
    l < 0 es ¬x_|l|. Rechaza (False) literales fuera de rango en lugar de
    fallar. Tiempo O(n + tamaño de la fórmula); espacio O(n).
    """
    if not isinstance(a, dict) or set(a) != set(range(1, n + 1)):
        return False
    if any(type(v) is not bool for v in a.values()):
        return False
    if any(not 1 <= abs(l) <= n for c in clauses for l in c):
        return False
    return all(any(a[abs(l)] == (l > 0) for l in c) for c in clauses)


def sat(clauses, n):
    """C1 · Búsqueda exacta por retroceso (backtracking).

    Asigna variables en orden y poda cuando alguna cláusula queda con todos
    sus literales asignados y falsos. La profundidad máxima es n, así que
    termina. Tiempo O(2^n (n + m)) en el peor caso; espacio O(n).
    Devuelve un dict (vacío si n = 0 y la fórmula es trivial) o None.
    """
    if n < 0 or any(len(c) > 3 or any(not 1 <= abs(l) <= n for l in c) for c in clauses):
        raise ValueError("CNF invalida")

    def buscar(a):
        if any(all(abs(l) in a and a[abs(l)] != (l > 0) for l in c) for c in clauses):
            return None                       # poda: cláusula ya falsa
        if len(a) == n:
            return dict(a)
        i = len(a) + 1
        for valor in (False, True):
            a[i] = valor
            r = buscar(a)
            if r is not None:
                return r
            del a[i]
        return None

    return buscar({})


def verify_tsp(D, L, path):
    """C2 · Verificador de TSP de decisión.

    Certificado: recorrido (0, ..., 0) que visita cada centro exactamente
    una vez y regresa al origen. Comprueba forma de la matriz, unicidad,
    retorno y costo <= L. Tiempo O(n) sobre el recorrido (más O(n) para
    validar filas); espacio O(n).
    """
    n = len(D)
    if n == 0 or any(len(fila) != n for fila in D):
        return False
    return (len(path) == n + 1 and path[0] == path[-1] == 0
            and set(path[:-1]) == set(range(n))
            and sum(D[u][v] for u, v in zip(path, path[1:])) <= L)


def tsp(D, L):
    """C2 · Búsqueda exacta: primer recorrido con costo <= L.

    Es la versión de decisión: no busca el mínimo, sino un tour factible.
    Fija el origen 0 y enumera (n-1)! órdenes; termina por finitud.
    Tiempo O((n-1)! n); espacio O(n) auxiliar más la matriz.
    """
    n = len(D)
    if n == 0 or any(len(fila) != n or any(w < 0 for w in fila) for fila in D):
        raise ValueError("Distancias invalidas")
    for p in permutations(range(1, n)):
        ruta = (0,) + p + (0,)
        if verify_tsp(D, L, ruta):
            return ruta, sum(D[u][v] for u, v in zip(ruta, ruta[1:]))
    return None


def verify_cover(V, E, k, S):
    """C3 · Verificador de Vertex Cover.

    Certificado: conjunto S ⊆ V con |S| <= k que toca cada arista. Rechaza
    aristas con extremos fuera de V. Tiempo O(V + E) esperado (hash);
    espacio O(V).
    """
    vertices = set(V)
    S = set(S)
    if any(u not in vertices or v not in vertices for u, v in E):
        return False
    return S <= vertices and len(S) <= k and all(u in S or v in S for u, v in E)


def cover(V, E, k):
    """C3 · Búsqueda exacta por subconjuntos de tamaño creciente.

    Prueba subconjuntos de tamaño 0..min(k, |V|) y devuelve el primero
    válido (por tanto, uno de tamaño mínimo) o None. Termina por finitud.
    Tiempo O(2^V (V + E)); espacio O(V + E).
    """
    V = list(dict.fromkeys(V))
    E = list(E)
    vertices = set(V)
    if k < 0 or any(u not in vertices or v not in vertices for u, v in E):
        raise ValueError("Grafo invalido")
    for tam in range(min(k, len(V)) + 1):
        for S in combinations(V, tam):
            if verify_cover(V, E, k, S):
                return set(S)
    return None
