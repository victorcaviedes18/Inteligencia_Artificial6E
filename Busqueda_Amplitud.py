from collections import deque
 
 
class Graph:
    
    def __init__(self, edges, n):
 
        self.adjList = [[] for _ in range(n)]
 
        
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.adjList[dest].append(src)
 
 

def BFS(graph, v, discovered):
 
    
    q = deque()
 
    
    discovered[v] = True
 
    
    q.append(v)
 
    
    while q:
 
        
        v = q.popleft()
        print(v, end=' ')
 
       
        for u in graph.adjList[v]:
            if not discovered[u]:
                
                discovered[u] = True
                q.append(u)
 
 
if __name__ == '__main__':
 
    
    edges = [
        (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (5, 9),
        (5, 10), (4, 7), (4, 8), (7, 11), (7, 12)
        
    ]
 
    
    n = 15
 
    
    graph = Graph(edges, n)
 
    
    discovered = [False] * n
 
    # Realizar el recorrido BFS de todos los nodos no descubiertos a
    # cubre todos los componentes conectados de un graph
    for i in range(n):
        if not discovered[i]:
            
            BFS(graph, i, discovered)