import json
import math
import unittest
from pathlib import Path
from datetime import date
from algoritmos.dijkstra import dijkstra
from algoritmos.fefo import fefo
from algoritmos.reposicion import reposicion, sugerencias

class Sprint2(unittest.TestCase):
    def setUp(self):
        self.g = json.loads((Path(__file__).resolve().parents[1] / "grafos/planta.json").read_text())
        self.aristas = self.g["aristas"]
        self.nodos = {v for u, w, p in self.aristas for v in (u,w)}
        self.hoy = date(2026,11,24)

    def test_ruta(self):
        costo, ruta = dijkstra(self.nodos,self.aristas,"R","D")
        self.assertEqual(costo,11)
        self.assertIn(ruta,[["R","B","A","E","D"],["R","B","A","P","E","D"]])

    def test_bloqueo(self):
        self.assertEqual(dijkstra(self.nodos,self.aristas,"R","D",bloqueados=["E"]),(math.inf,[]))

    def test_origen_destino(self):
        self.assertEqual(dijkstra(self.nodos,self.aristas,"R","R"),(0,["R"]))

    def test_peso_invalido(self):
        with self.assertRaises(ValueError):
            dijkstra(self.nodos,[["R","D",-1]],"R","D")

    def test_fefo(self):
        lotes = [("B",date(2026,11,25),4),("A",date(2026,11,25),3),("X",date(2026,11,23),99)]
        self.assertEqual(fefo(lotes,5,self.hoy),{"completo":True,"plan":[("A",3),("B",2)],"pendiente":0})

    def test_fefo_insuficiente(self):
        self.assertEqual(fefo([],5,self.hoy),{"completo":False,"plan":[],"pendiente":5})

    def test_fefo_cero(self):
        self.assertTrue(fefo([],0,self.hoy)["completo"])

    def test_fefo_invalido(self):
        with self.assertRaises(ValueError):
            fefo([], -1,self.hoy)

    def test_reposicion(self):
        self.assertEqual(reposicion(18,10,5,30,50),(23,27))

    def test_reposicion_limite(self):
        self.assertEqual(reposicion(30,0,0,30,50),(30,20))
        self.assertEqual(reposicion(31,0,0,30,50),(31,0))

    def test_reposicion_orden_abierta(self):
        self.assertEqual(reposicion(18,37,5,30,50),(50,0))

    def test_reposicion_invalida(self):
        with self.assertRaises(ValueError):
            reposicion(-1,0,0,30,50)

    def test_sku_duplicado(self):
        with self.assertRaises(ValueError):
            list(sugerencias([("A",18,10,5,30,50)]*2))

if __name__ == "__main__":
    unittest.main()
