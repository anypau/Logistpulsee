# LOGISTPULSE — Teoría de la Computación

Universidad San Francisco de Quito · Deber 2

Integrantes: Ana Paula Lopez y Felipe Armas.

## Sprints
- [Sprint 1: autómatas y grafo](sprints/sprint1.md)
- [Sprint 2: Dijkstra, FEFO y reposición](sprints/sprint2.md)
- [Sprint 3: diez correos, P, NP y NP-completitud](sprints/sprint3.md)
- [Distribución de responsabilidades](sprints/contribuciones.md)
- [Revisión técnica de Felipe](sprints/revision_felipe.md)
- [Retrospectivas](retrospectivas.md)

## Ejecución reproducible
Python 3.10+; sin dependencias externas. Desde la raíz del repositorio:
```bash
python -m unittest discover -s tests -v
```

Abrir los tres archivos .jff de [automatas](automatas/) en JFLAP 7.1, seleccionar Input > Multiple Run e introducir las cadenas de prueba de Sprint 1. Comparar con los resultados esperados.

## Resultados y evidencias
| Grupo | Pruebas | Resultado documentado |
|---|---:|---|
| JFLAP: pedido, reserva y compra | 12 | 12 correctas |
| Python: Sprint 2 | 13 | 13 correctas |
| Python: Sprint 3 | 10 | 10 correctas |
| Total | 35 | 35 correctas |

- [Capturas JFLAP](evidencias/jflap/)
- [Captura de ejecución Python](evidencias/pruebas_python.png)
- [Código fuente](algoritmos/), [pruebas](tests/) y [grafo](grafos/).

Los resultados anteriores corresponden a las evidencias registradas; no garantizan corrección para todas las entradas.

## Informe, presentación y versión
- [Decidibilidad y parada](informes/decidibilidad.md)
- [Guion de exposición](presentacion/guion.md)
- [Release v1.0.0](https://github.com/anypau/Logistpulsee/releases/tag/v1.0.0)

El informe final y la presentación en PDF se entregan por separado junto al enlace del repositorio. El release v1.0.0 está publicado; las actualizaciones posteriores de documentación se registran en el historial de la rama principal.

## Cierre de gestión
La distribución de responsabilidades y las retrospectivas están documentadas. La confirmación individual de aportes y reflexiones, así como las fechas de revisión por pares, corresponde a los integrantes. No se atribuyen reuniones o aprobaciones no verificadas.
