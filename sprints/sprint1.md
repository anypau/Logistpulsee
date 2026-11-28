# Sprint 1 — Formalización y pruebas

AFD parcial: toda transición no definida rechaza (equivale a un sumidero no final). Un estado final indica cierre del proceso, no necesariamente éxito.

## Pedido
Q = {q0 Borrador, q1 Confirmado, q2 Reservado, q3 Preparacion, q4 Empacado, q5 Despachado, q6 Entregado, q7 Cancelado}.
Σ = {c confirmar, r reservar, i iniciar picking, e empacar, d despachar, t entregar, x cancelar}.
Inicial q0; F = {q6,q7}.
δ: q0,c→q1; q1,r→q2; q2,i→q3; q3,e→q4; q4,d→q5; q5,t→q6; q0,x→q7; q1,x→q7; q2,x→q7.

| Cadena | Resultado esperado | Traza |
|---|---|---|
| criedt | Aceptada | 0→1→2→3→4→5→6 |
| crx | Aceptada | 0→1→2→7 |
| d | Rechazada | 0, sin transición d |
| cret | Rechazada | 0→1→2, sin transición e |

## Reserva
Q = {q0 Solicitada, q1 Validada, q2 Reservada, q3 Consumida, q4 Liberada, q5 Expirada, q6 Rechazada}.
Σ = {v validar, s sin stock, c confirmar, p picking, x cancelar, z vence plazo}.
Inicial q0; F = {q3,q4,q5,q6}.
δ: q0,v→q1; q0,s→q6; q1,c→q2; q2,p→q3; q2,x→q4; q2,z→q5.

| Cadena | Resultado esperado | Traza |
|---|---|---|
| vcp | Aceptada | 0→1→2→3 |
| vcx | Aceptada | 0→1→2→4 |
| p | Rechazada | 0, sin transición p |
| vp | Rechazada | 0→1, sin transición p |

## Compra
Q = {q0 Borrador, q1 En aprobacion, q2 Aprobada, q3 Enviada, q4 Recepcion parcial, q5 Recibida, q6 Rechazada}.
Σ = {s solicitar aprobación, a aprobar, r rechazar, e emitir orden, p recibir parte, c recibir completa, t completar recepción}.
Inicial q0; F = {q5,q6}.
δ: q0,s→q1; q1,a→q2; q1,r→q6; q2,e→q3; q3,p→q4; q3,c→q5; q4,t→q5.

| Cadena | Resultado esperado | Traza |
|---|---|---|
| saept | Aceptada | 0→1→2→3→4→5 |
| sr | Aceptada | 0→1→6 |
| e | Rechazada | 0, sin transición e |
| sre | Rechazada | 0→1→6, sin transición e |

## Grafo
Modelo no dirigido, pesos en metros, origen R, destino D. Ruta mínima R→B→A→E→D, costo 11 m. También R→B→A→P→E→D cuesta 11 m. Bloquear E desconecta D. Dijkstra requiere pesos no negativos. Con lista de adyacencia y cola de prioridad indexada: O((V+E) log V) tiempo y O(V+E) espacio incluyendo el grafo.

## Gestión y cierre
Backlog: formalizar los tres autómatas, probar doce secuencias en JFLAP, guardar evidencias y definir el grafo de planta.

Responsabilidades asignadas según [contribuciones](contribuciones.md): Ana Paula Lopez — autómatas y pruebas JFLAP; Felipe Armas — grafo y formalización.

Resultado documentado: 12 de 12 pruebas JFLAP correctas. [Capturas](../evidencias/jflap/).

Revisión técnica: contrastar las cadenas esperadas con las capturas y verificar la ruta de 11 m. Consultar [revisión de Felipe](revision_felipe.md) y [retrospectivas del equipo](../retrospectivas.md). La confirmación individual de aportes, reflexiones y fechas de revisión corresponde a los integrantes.
