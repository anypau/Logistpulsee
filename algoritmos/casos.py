from collections import deque
from itertools import permutations, combinations
from heapq import heappush, heappop
from math import inf

def bfs(edges,s,t):
    g={}
    for u,v in edges: g.setdefault(u,[]).append(v)
    q=deque([s]); seen={s}
    while q:
        u=q.popleft()
        if u==t:return True
        for v in g.get(u,[]):
            if v not in seen:seen.add(v);q.append(v)
    return False

def shortest(edges,s):
    g={s:[]}
    for u,v,w in edges:
        if w<0:raise ValueError("Peso negativo")
        g.setdefault(u,[]).append((v,w));g.setdefault(v,[])
    d=dict.fromkeys(g,inf);d[s]=0;prev={};q=[(0,s)]
    while q:
        a,u=heappop(q)
        if a!=d[u]:continue
        for v,w in g[u]:
            if a+w<d[v]:d[v]=a+w;prev[v]=u;heappush(q,(d[v],v))
    return d,prev

def maxflow(edges,s,t):
    if s==t:raise ValueError("Origen igual a destino")
    r={s:{},t:{}}
    for u,v,c in edges:
        if type(c)!=int or c<0:raise ValueError("Capacidad invalida")
        r.setdefault(u,{});r.setdefault(v,{})
        r[u][v]=r[u].get(v,0)+c;r[v].setdefault(u,0)
    total=0;log=[]
    while True:
        p={s:None};q=deque([s])
        while q and t not in p:
            u=q.popleft()
            for v,c in r[u].items():
                if c>0 and v not in p:p[v]=u;q.append(v)
        if t not in p:return total,log
        path=[t]
        while path[-1]!=s:path.append(p[path[-1]])
        path.reverse();pairs=list(zip(path,path[1:]))
        c=min(r[u][v] for u,v in pairs)
        for u,v in pairs:r[u][v]-=c;r[v][u]+=c
        total+=c;log.append((path,c))

def matrix(A):
    if any(len(row)!=len(A) or any(x not in (0,1) for x in row) for row in A):raise ValueError("Matriz invalida")

def verify_iso(A,B,p):
    matrix(A);matrix(B);n=len(A)
    return len(B)==n and len(p)==n and set(p)==set(range(n)) and all(A[i][j]==B[p[i]][p[j]] for i in range(n) for j in range(n))

def iso(A,B,nontrivial=False):
    matrix(A);matrix(B)
    if len(A)!=len(B):return None
    for p in permutations(range(len(A))):
        if nontrivial and p==tuple(range(len(A))):continue
        if verify_iso(A,B,p):return p
    return None

def verify_auto(A,p):
    return tuple(p)!=tuple(range(len(A))) and verify_iso(A,A,p)

def verify_factor(N,B,d):
    return type(d)==int and 2<=d<=B and N%d==0

def factor(N,B):
    if N<2 or B<0:raise ValueError("Parametros invalidos")
    return next((d for d in range(2,min(B,N)+1) if verify_factor(N,B,d)),None)

def verify_log(p,g,h,B,x):
    return type(x)==int and 0<=x<=B and pow(g,x,p)==h

def discrete(p,g,h,B):
    # Precondicion: p primo; residuos canonicos.
    if p<2 or not 0<=g<p or not 0<=h<p or B<0:raise ValueError("Parametros invalidos")
    v=1%p
    for x in range(B+1):
        if v==h:return x
        v=v*g%p
    return None

def verify_sat(clauses,n,a):
    return set(a)==set(range(1,n+1)) and all(type(v)==bool for v in a.values()) and all(any(a[abs(l)]==(l>0) for l in c) for c in clauses)

def sat(clauses,n):
    if n<0 or any(len(c)>3 or any(not 1<=abs(l)<=n for l in c) for c in clauses):raise ValueError("CNF invalida")
    def search(a):
        if any(all(abs(l) in a and a[abs(l)]!=(l>0) for l in c) for c in clauses):return None
        if len(a)==n:return dict(a)
        i=len(a)+1
        for bit in (False,True):
            a[i]=bit
            r=search(a)
            if r is not None:return r
            del a[i]
        return None
    return search({})

def verify_tsp(D,L,path):
    n=len(D)
    return n>0 and len(path)==n+1 and path[0]==path[-1]==0 and set(path[:-1])==set(range(n)) and sum(D[u][v] for u,v in zip(path,path[1:]))<=L

def tsp(D,L):
    n=len(D)
    if n==0 or any(len(row)!=n or any(w<0 for w in row) for row in D):raise ValueError("Distancias invalidas")
    for p in permutations(range(1,n)):
        path=(0,)+p+(0,)
        if verify_tsp(D,L,path):return path,sum(D[u][v] for u,v in zip(path,path[1:]))
    return None

def verify_cover(V,E,k,S):
    S=set(S)
    return S<=set(V) and len(S)<=k and all(u in S or v in S for u,v in E)

def cover(V,E,k):
    V=list(dict.fromkeys(V));E=list(E)
    if k<0 or any(u not in V or v not in V for u,v in E):raise ValueError("Grafo invalido")
    for i in range(min(k,len(V))+1):
        for S in combinations(V,i):
            if verify_cover(V,E,k,S):return set(S)
    return None
