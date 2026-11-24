# Sprint 3 — Correos y complejidad

Fuente: simulador LOGISTPULSE, casos p1–c3. Modelo: algoritmo determinista sobre entradas finitas codificadas; las versiones de decisión de los diez casos son decidibles. Las búsquedas son exactas, no heurísticas. P ⊆ NP; pertenecer a NP no demuestra dureza. Los casos de optimización se clasifican mediante su versión de decisión.

## Fichas

### P1 — Daniela Paredes: pedidos alcanzables
Entrada: grafo dirigido de rutas activas, origen Durán y destino Norte. Salida: sí/no. BFS explora cada nodo alcanzable una vez; al vaciar la cola concluye no. P por O(V+E) tiempo, O(V) auxiliar (O(V+E) incluyendo construcción del grafo). Caso del expediente: Durán→Quito→Norte, sí. Invertir origen/destino: no. Código bfs, prueba test_p1.

### P2 — Marco Cedeño: ruta de menor tiempo
Entrada: grafo dirigido con pesos no negativos; origen Quito. Optimización: distancias y predecesores; decisión: ¿distancia al destino ≤ L? Dijkstra es exacto porque al extraer una distancia mínima vigente queda fijada. Termina tras finitas relajaciones. P, O((V+E) log V) en grafo simple con heap; O(V+E) espacio incluyendo heap y grafo. Pesos negativos invalidan la prueba de correctitud. Distancias Quito 0, Latacunga 2, Ambato 5, Guayaquil 8; Quito→Latacunga→Guayaquil y Quito→Ambato→Guayaquil empatan. Código shortest, test_p2.

### P3 — Luis Vaca: capacidad máxima
Entrada: red dirigida con capacidades enteras no negativas, planta y clientes. Optimización: máximo flujo; decisión: ¿flujo ≥ K? Edmonds–Karp usa BFS residual, actualiza aristas inversas y termina cuando no hay camino aumentante; por máximo flujo/corte mínimo el resultado es óptimo. O(VE²) tiempo, O(V+E) espacio, sin contar registro de aumentos (hasta O(V²E) elementos). Caso: Planta→Quito→Clientes: 4; Planta→Guayaquil→Clientes: 5; Planta→Quito→Guayaquil→Clientes: 1. Total 10, igual a capacidad del corte de entrada a Clientes. Código maxflow, test_p3.

### N1 — Elena Ruiz: isomorfismo
Entrada: dos matrices de adyacencia de n vértices; salida sí/no. Certificado: permutación p de 0..n−1. Verificar biyección y A[i,j]=B[p(i),p(j)] para todos los pares, O(n²) tiempo, O(n) auxiliar. Certificado O(n log n) bits. NP por verificación polinómica, sin afirmar NP-completitud. Enumeración exacta de n! permutaciones termina; O(n! n²) tiempo, O(n) auxiliar (matrices O(n²)). Para matrices de ejemplo del simulador, p=(1,0,2). Código iso y verify_iso, test_n1.

### N2 — Andrés Molina: divisor acotado
Entrada: N≥2 y B≥0 enteros binarios. ¿Existe d con 2≤d≤B y N mod d=0? Certificado d, longitud O(log N) si d divide N. Verificador comprueba rango y residuo. NP; no se afirma dureza. Enumeración hasta min(B,N) termina. Sea b longitud binaria total; división escolar O(b²), búsqueda O(min(B,N) b²) tiempo y O(b) bits de almacenamiento auxiliar aritmético bajo división escolar. Puede ser exponencial en b. Verificación O(b²). N=91,B=10: d=7; 3 inválido. Código factor y verify_factor, test_n2.

### N3 — Paola León: logaritmo discreto acotado
Entrada: primo p, residuos canónicos g,h, B≥0 binario. ¿Existe 0≤x≤B con g^x mod p=h? Certificado x de O(log(B+1)) bits. Exponenciación rápida verifica en O(log(B+1)·b²) operaciones de bit (b=longitud de p, aritmética escolar; agregar lectura de entrada). NP sin afirmar dureza. Búsqueda exacta incremental mantiene v=g^x mod p; O((B+1)b²) operaciones aritméticas de bit más costo de contador, O(b+log(B+1)) bits de trabajo. Termina al alcanzar B. p=23,g=5,h=8,B=10: x=6. Código discrete y verify_log, test_n3. Primalidad es precondición del expediente.

### N4 — Santiago Jaramillo: automorfismo no trivial
Entrada: matriz A de n vértices. ¿Existe permutación p distinta de identidad que preserve A? Certificado p; verificar biyección, no identidad y adyacencias en O(n²), O(n) auxiliar. NP. Enumerar n! permutaciones termina; O(n! n²), O(n) auxiliar. Triángulo: p=(0,2,1). Un vértice no tiene automorfismo no trivial. Código iso con nontrivial=True, verify_auto, test_n4.

### C1 — Mónica Ruiz: SAT
Entrada: fórmula CNF con n variables y m cláusulas de hasta 3 literales. ¿Existe asignación que satisfaga todas? Certificado n bits; verificación O(n+m) tiempo y O(n) auxiliar. NP-hard: 3-SAT conocido NP-completo se transforma por identidad (mismas variables, cláusulas y satisfacibilidad), en tiempo lineal. Por ambas propiedades es NP-completo. Retroceso exacto con poda de cláusulas falsas, termina a profundidad n. Tiempo O(2^n(n+m)), espacio O(n) auxiliar más fórmula. Ejemplo (x1∨¬x2)∧(x2∨x3): (F,F,V) satisface. Fórmula x1∧¬x1 no. Las cláusulas de ejemplo de dos literales pueden rellenarse repitiendo un literal si se exige exactamente tres. Código sat y verify_sat, test_c1.

### C2 — Jorge Tapia: TSP de decisión
Entrada: matriz simétrica de distancias no negativas y límite L. ¿Existe ciclo que visite cada centro una vez y regrese con costo ≤L? Certificado: orden de n centros, O(n log n) bits; verificar unicidad, retorno y costo en O(n) operaciones aritméticas, O(n) auxiliar. NP-hard: desde ciclo hamiltoniano no dirigido de n vértices, construir matriz completa con peso 1 si existe arista y 2 si no, diagonal 0, L=n. Un tour de n aristas cuesta ≤n exactamente si todas son originales, equivalente a ciclo hamiltoniano. Construcción O(n²); NP-completo. Enumeración de (n−1)! tours fijando origen, termina; O(n! ) operaciones, O(n) auxiliar más matriz O(n²). Con pesos binarios sumar/comparar agrega factor polinómico en sus bits. Matriz del ejemplo: 0→1→2→0 cuesta 15≤20; con L=14 no. La búsqueda devuelve cualquier tour factible, no necesariamente mínimo. Código tsp y verify_tsp, test_c2.

### C3 — Carla Núñez: Vertex Cover
Entrada: grafo no dirigido G=(V,E), entero k. ¿Existe S⊆V, |S|≤k, con al menos un extremo de cada arista en S? Certificado conjunto S; O(V+E) tiempo esperado y O(V) auxiliar con hash. NP-hard por reducción identidad desde Vertex Cover conocido NP-completo: zonas=vértices, corredores=aristas, equipos=k. Se conserva la respuesta sí/no. NP-completo. Enumeración de subconjuntos hasta k, exacta, finita; O(2^V(V+E)) tiempo, O(V+E) espacio incluyendo grafo. A-B, B-C, k=1: {B}; k=0 no. Se usa el requisito explícito del correo (cubrir corredores); la descripción genérica del portal sobre cubrir cada zona propia o vecina correspondería a Dominating Set y no es equivalente. Código cover y verify_cover, test_c3.

## Tabla resumen
| Caso | Evidencia | Algoritmo exacto | Tiempo |
|---|---|---|---|
| P1 | P | BFS | O(V+E) |
| P2 | P | Dijkstra | O((V+E) log V) |
| P3 | P | Edmonds–Karp | O(VE²) |
| N1 | NP | Permutaciones | O(n! n²) |
| N2 | NP | División | O(min(B,N)b²) |
| N3 | NP | Iteración modular | O((B+1)b²), más contador |
| N4 | NP | Permutaciones | O(n! n²) |
| C1 | NP-completo | Retroceso | O(2^n(n+m)) |
| C2 | NP-completo | Permutaciones | O(n!) operaciones |
| C3 | NP-completo | Subconjuntos | O(2^V(V+E)) |

Todos decidibles. Ejecutar desde raíz: python -m unittest discover -s tests -v. Los valores anteriores son resultados esperados, no un registro de ejecución. Revisión y retrospectiva reales pendientes.
