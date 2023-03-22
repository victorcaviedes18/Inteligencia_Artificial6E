from queue import PriorityQueue

def heuristic(a, b):
    # calcula la distancia euclidiana entre dos puntos
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def a_star_search(start, end, graph):
    # crea una cola de prioridad para almacenar los nodos
    frontier = PriorityQueue()
    frontier.put(start, 0)
    # crea un diccionario para almacenar el costo del camino desde el inicio hasta cada nodo
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    # comienza la búsqueda
    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from, cost_so_far

class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    def in_bounds(self, pos):
        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height
    def passable(self, pos):
        return pos not in self.walls
    def neighbors(self, pos):
        (x, y) = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
    def cost(self, current, next):
        return 1

# Ejemplo de uso
g = Graph(10, 10)
g.walls = [(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (5, 4)]
start = (0, 0)
end = (7, 7)
came_from, cost_so_far = a_star_search(start, end, g)

# Imprime el mejor camino encontrado
current = end
while current != start:
    print(current)
    current = came_from[current]
print(start)

