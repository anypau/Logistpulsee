import unittest
from algoritmos.casos import *

class Correos(unittest.TestCase):
    def test_p1(self):
        e=[("Durán","Quito"),("Durán","Guayaquil"),("Quito","Norte"),("Guayaquil","Sur")]
        self.assertTrue(bfs(e,"Durán","Norte"))
        self.assertFalse(bfs(e,"Norte","Durán"))
    def test_p2(self):
        e=[("Quito","Latacunga",2),("Quito","Ambato",5),("Latacunga","Guayaquil",6),("Ambato","Guayaquil",3)]
        d,p=shortest(e,"Quito")
        self.assertEqual(d,{"Quito":0,"Latacunga":2,"Ambato":5,"Guayaquil":8})
        self.assertEqual(p["Guayaquil"],"Latacunga")
        with self.assertRaises(ValueError):shortest([("A","B",-1)],"A")
    def test_p3(self):
        e=[("Planta","Quito",7),("Planta","Guayaquil",5),("Quito","Clientes",4),("Guayaquil","Clientes",6),("Quito","Guayaquil",2)]
        f,log=maxflow(e,"Planta","Clientes")
        self.assertEqual(f,10)
        self.assertEqual(sum(c for _,c in log),10)
        self.assertEqual(maxflow([],"A","B")[0],0)
        with self.assertRaises(ValueError):maxflow([("A","B",-1)],"A","B")
    def test_n1(self):
        A=[[0,1,0],[1,0,1],[0,1,0]]
        B=[[0,1,1],[1,0,0],[1,0,0]]
        self.assertTrue(verify_iso(A,B,iso(A,B)))
        self.assertIsNone(iso(A,[[0]*3 for _ in range(3)]))
        self.assertFalse(verify_iso(A,B,(0,0,1)))
    def test_n2(self):
        self.assertEqual(factor(91,10),7)
        self.assertTrue(verify_factor(91,10,7))
        self.assertFalse(verify_factor(91,10,3))
        self.assertIsNone(factor(13,10))
        self.assertFalse(verify_factor(0,10,7))  # N fuera de dominio
    def test_n3(self):
        self.assertEqual(discrete(23,5,8,10),6)
        self.assertTrue(verify_log(23,5,8,10,6))
        self.assertFalse(verify_log(23,5,8,10,5))
        self.assertIsNone(discrete(23,5,8,5))
        self.assertFalse(verify_log(0,5,8,10,6))  # modulo invalido
    def test_n4(self):
        A=[[0,1,1],[1,0,1],[1,1,0]]
        self.assertTrue(verify_auto(A,iso(A,A,True)))
        self.assertFalse(verify_auto(A,(0,1,2)))
        self.assertIsNone(iso([[0]],[[0]],True))
    def test_c1(self):
        C=[[1,-2],[2,3]]
        self.assertTrue(verify_sat(C,3,sat(C,3)))
        self.assertIsNone(sat([[1],[-1]],1))
        self.assertFalse(verify_sat(C,3,{1:False,2:True,3:False}))
        self.assertFalse(verify_sat([[4]],3,{1:True,2:True,3:True}))  # literal fuera de rango
    def test_c2(self):
        D=[[0,4,8],[4,0,3],[8,3,0]]
        p,c=tsp(D,20)
        self.assertEqual(c,15)
        self.assertTrue(verify_tsp(D,20,p))
        self.assertIsNone(tsp(D,14))
        self.assertFalse(verify_tsp(D,20,(0,1,1,0)))
        self.assertFalse(verify_tsp([[0,1],[1]],20,(0,1,0)))  # matriz no cuadrada
    def test_c3(self):
        V=["A","B","C"];E=[("A","B"),("B","C")]
        self.assertEqual(cover(V,E,1),{"B"})
        self.assertTrue(verify_cover(V,E,1,{"B"}))
        self.assertFalse(verify_cover(V,E,1,{"A"}))
        self.assertIsNone(cover(V,E,0))
        self.assertFalse(verify_cover(V,E+[("B","Z")],1,{"B"}))  # extremo fuera de V

if __name__=="__main__":unittest.main()
