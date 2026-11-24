# Sprint 2 — Algoritmos logísticos

## Dijkstra
Entrada: vértices, aristas ponderadas, origen, destino, dirección y zonas bloqueadas. Salida: costo mínimo y ruta, o infinito y lista vacía. Pesos finitos no negativos. Se excluyen aristas incidentes a zonas bloqueadas.

Pseudocódigo:
    dist[v] = infinito para cada v; dist[origen] = 0
    insertar (0, origen) en min-heap
    mientras heap no vacío:
        extraer (d,u); ignorar si d != dist[u]
        si u es destino: reconstruir con predecesores y devolver
        para cada vecino v con peso w:
            si d+w < dist[v]:
                dist[v] = d+w; pred[v] = u; insertar (dist[v],v)
    devolver infinito, ruta vacía

Correctitud: al extraer una distancia vigente mínima, los pesos no negativos garantizan que no existe un camino más corto aún pendiente. Termina porque cada arista se examina como máximo una vez por extremo asentado y cada mejora genera una inserción finita. Es exacto. Con heap indexado: O((V+E) log V); la implementación heapq permite entradas obsoletas, por lo que su cota general es O(V+E log(E+1)); para grafos simples equivale a O((V+E) log V). Espacio O(V+E), incluyendo grafo y heap.

## FEFO
Entrada: L lotes (código, fecha de vencimiento, cantidad disponible), fecha actual y demanda entera no negativa. Salida: plan, faltante y estado completo.

Pseudocódigo:
    validar lotes y demanda
    filtrar lotes con vencimiento >= hoy y disponible > 0
    ordenar por (fecha, código)
    pendiente = demanda; plan = []
    para cada lote ordenado mientras pendiente > 0:
        tomar = min(pendiente, disponible)
        agregar (código, tomar); pendiente -= tomar
    devolver plan, pendiente y (pendiente == 0)

Se supone que un lote vence al finalizar su fecha indicada. Si falta stock, se devuelve plan parcial informativo y no se reserva nada hasta autorización. Desempate lexicográfico por código. Termina tras recorrer un máximo de L lotes. Tiempo O(L log L), espacio O(L). Selección exacta respecto de la política FEFO, no optimización de otros objetivos.

## Reposición
Entrada: P SKU con disponible, en orden, reservado, mínimo y objetivo. Salida: posición y sugerencia por SKU.

Pseudocódigo:
    para cada SKU:
        posición = disponible + en_orden - reservado
        si posición <= mínimo:
            sugerencia = max(0, objetivo - posición)
        si no: sugerencia = 0
        emitir SKU, posición, sugerencia

Termina tras P filas. Tiempo O(P) esperado con conjunto hash; la regla por SKU usa O(1) espacio. La implementación valida SKU únicos con O(P) espacio adicional. Las órdenes abiertas se incluyen en la posición; al confirmar una nueva orden se debe actualizar en_orden de forma atómica antes de recalcular, evitando duplicación por ejecuciones concurrentes. No se crean órdenes automáticamente.

## Pruebas
Desde la raíz: python -m unittest discover -s tests -p "test_sprint2.py" -v

Casos normales: ruta de 11 m, FEFO con desempate, reposición de 27 unidades.
Casos límite: destino igual al origen, bloqueo de E, stock insuficiente, demanda cero, posición igual al mínimo, orden abierta.
Casos inválidos: peso negativo, demanda negativa, inventario negativo y SKU duplicado.

## Gestión
Backlog: implementar Dijkstra, FEFO, reposición, pruebas y análisis. Revisión por pares y retrospectiva pendientes de realizar y registrar por el equipo. No se simula evidencia de reuniones.
