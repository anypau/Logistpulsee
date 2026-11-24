# Grafo ponderado

No dirigido; pesos en metros. Origen R, destino D. Sin bloqueos en el caso base.

```mermaid
graph LR
R ---|4| A
R ---|2| B
A ---|1| B
A ---|3| P
A ---|5| E
B ---|7| P
B ---|3| C
P ---|2| C
P ---|2| E
C ---|4| E
E ---|3| D
```

Ruta mínima R → B → A → E → D, costo 11 m. También R → B → A → P → E → D cuesta 11 m. Si E se bloquea, D queda aislado.
