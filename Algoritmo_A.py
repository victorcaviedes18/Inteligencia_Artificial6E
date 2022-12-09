import os
import math
from random import randint
import time


# Definir variables globales
gz_char = '█'  # Definir el carácter de cuadrícula predeterminado
fruit_char = '★'  # Definir caracteres de visualización de frutas
self_char = '●'  # Define tus propios personajes para mostrar
wall_char = '◆'  # Definir caracteres de visualización de pared

# Todo el proceso utiliza la dirección hacia arriba y hacia abajo como la dirección x positiva (la dirección de aumentar el índice de la línea de lista bidimensional)
# Use la dirección de izquierda a derecha para todo el proceso como la dirección y positiva (la dirección del aumento del índice de columna de lista bidimensional)


class Map2D(object):
    '' 'Clase de mapa 2D' ''

    def __init__(self, width=20, height=20):
        'Inicializacion'
        'Args:' 
        '                 ancho mapa ancho'
        '                 altura mapa altura'
        
        self.width = width
        self.height = height
        self.char = gz_char  # Caracteres predeterminados del mapa
        # Generar mapa
        self.map = [[self.char for col in range(
            self.width)] for row in range(self.height)]
        # Generar un muro alrededor del mapa
        self.wall = [[i, j] for j in [-1, self.width] for i in range(self.height)] + [
            [j, i] for j in [-1, self.height] for i in range(-1, self.width + 1)]

    def __getitem__(self, item):
        '' 'Valor por clave' ''
        return self.map[item]

    def __setitem__(self, key, value):
        '' 'Guardar valor por clave' ''
        self.map[key] = value

    def show(self):
        '' 'Imprimir el mapa actual en la consola' ''
        for row in self.map:
            for c in row:
                # Use el control de color de la consola para distinguir
                if c == self_char:
                    print('\033[1;35;44m' + c + '\033[0m', end='')
                elif c == wall_char:
                    print('\033[0;36;41m' + c + '\033[0m', end='')
                elif c == fruit_char:
                    print('\033[1;33;40m' + c + '\033[0m', end='')
                else:
                    print('\033[0;37;41m' + c + '\033[0m', end='')
            print()
        # Reiniciar el mapa, no habrá seguimiento de movimiento después de reiniciar
        # self.reload()

    def reload(self):
        '' 'Restablecer mapa' ''
        self.map = [[self.char for col in range(
            self.width)] for row in range(self.height)]


class AStar(object):
    '' 'Implementar un algoritmo de estrella' ''

    class Node(object):
        '' 'Clase de nodo' ''

        def __init__(self, x, y, parent_node=None):
            self.x = x
            self.y = y
            self.parent = parent_node  # Nodo principal
            # F = G + H
            # G = el costo de moverse desde el punto de partida A al cuadrado especificado
            # H = El costo estimado de mudarse del cuadrado especificado al destino B. Heurística Aquí se usa el método Manhattan para estimar H
            self.G = 0
            self.H = 0

    def __init__(self, map2D):
        '' 'inicialización' ''
        self.map = map2D

    def MinF(self):

        'Eliminar el nodo con la F más pequeña de open_list'
        'Returns:'
        'minF devuelve el nodo con el valor F más pequeño en open_list'        
        # Primero suponga que el primero es el más pequeño, luego seleccione el nodo con la F más pequeña en un bucle  
        minF = self.open_list[0]
        for node in self.open_list:
            if (node.G + node.H) <= (minF.G + minF.H):
                minF = node
        return minF

    def in_close_list(self, x, y):
        '' 'Juzgue si las coordenadas están en close_list'
        'Args:'
        'x x coordenada'
        '               coordenada y'
        'Return:'
        'nodo Si las coordenadas están en close_list, devuelve el nodo, de lo contrario devuelve False'
        
        for node in self.close_list:
            if node.x == x and node.y == y:
                return node
        return False

    def in_open_list(self, x, y):
        'Juzgue si las coordenadas están en open_list'
        'Args:'
        'x x coordenada'
        '                  coordenada y'
        ' Return:'
        '                  nodo Si las coordenadas están en open_list, devuelve el nodo, de lo contrario devuelve False'
        
        for node in self.close_list:
            if node.x == x and node.y == y:
                return node
        return False

    def search(self, node):
        'Buscar en el camino circundante'
        'Args:'
        '                 nodo de búsqueda nodo'
        
        # Determine si el nodo modificado es un obstáculo (obstáculo o muro)
        if [node.x, node.y] in self.obstacles:
            # Ignora el camino si es un obstáculo
            return
        # Determinar si está en close_list
        if self.in_close_list(node.x, node.y):
            # Ignora el nodo si ya está en close_list
            return
        # Calcular G y H
        node.G = node.parent.G + 10
        node.H = abs(self.target_node.x - node.x) + \
            abs(self.target_node.y - node.y) * 10
        # Determinar si está en open_list
        tmp = self.in_close_list(node.x, node.y)
        if tmp:
            # En open_list
            # Comparar F actual con F en lista_abierta
            if (node.G + node.H) < (tmp.G + tmp.H):
                # Si se juzga si el valor F de la ruta es menor que el valor F de la misma coordenada existente en la lista abierta
                tmp = node
        else:
            # No en open_list, agregar a open_list
            self.open_list.append(node)

    def start(self, current_position, target_positiion, obstacles):
        'Calcular la ruta óptima de una estrella'
        'Args:'
        '                 posición actual coordenadas de posición actual'
        '                 posición_objetivo coordenadas de posición objetivo'
        '                 lista de obstáculos de coordenadas de obstáculos'
        'Returns:'
        '               ruta_lista Si hay una ruta óptima, devuelva la ruta óptima estrella A, de todos modos, devuelva Ninguno'
         
        # Nodo de destino
        self.target_node = AStar.Node(*target_positiion)
        # Nodo actual
        self.current_node = AStar.Node(*current_position)
        # Abra la tabla, agregue el nodo actual a open_list
        self.open_list = [self.current_node]
        # Cerrar la mesa
        self.close_list = []
        # Conjunto de coordenadas de obstáculo (obstáculo real + muro)
        self.obstacles = obstacles + self.map.wall
        # Active un bucle de cálculo de estrella
        while True:
            # Determine si se alcanza el punto final, determine si las coordenadas del nodo objetivo están en la lista de cierre
            tmp = self.in_close_list(self.target_node.x, self.target_node.y)
            if tmp:
                # Regresar a la ruta
                path_list = [[tmp.x, tmp.y]]
                # Ruta inversa
                while tmp.parent:
                    tmp = tmp.parent
                    path_list.append([tmp.x, tmp.y])
                # Lista inversa
                path_list.reverse()
                return path_list
            if not self.open_list:
                # Si open_list está vacío, no hay forma de ir
                return None
            # Seleccione el nodo de ruta mínima F de open_list
            minF = self.MinF()
            # Agregue el nodo seleccionado actualmente a close_list y elimínelo de open_list
            self.close_list.append(minF)
            self.open_list.remove(minF)
            # Busque la ruta y utilice el nodo actual como nodo principal para buscar de acuerdo con un orden fijo (fijo en la línea, en cualquier orden)
            self.search(AStar.Node(minF.x - 1, minF.y, minF))
            self.search(AStar.Node(minF.x, minF.y - 1, minF))
            self.search(AStar.Node(minF.x + 1, minF.y, minF))
            self.search(AStar.Node(minF.x, minF.y + 1, minF))
            # Hay un largo tiempo de cálculo para borrar, imprima el mensaje de solicitud
            print('\\\\\\\\' 'Mao, planeando camino ... ', end='')

    def sub_start(self, current_position, target_positiion, obstacles, num=20):
        '' 'Limite el número de veces para juzgar si hay un camino por recorrer' ''
        # Nodo de destino
        self.target_node = AStar.Node(*target_positiion)
        # Nodo actual
        self.current_node = AStar.Node(*current_position)
        # Abra la tabla, agregue el nodo actual a open_list
        self.open_list = [self.current_node]
        # Cerrar la mesa
        self.close_list = []
        # Conjunto de coordenadas de obstáculo (obstáculo real + muro)
        self.obstacles = obstacles + self.map.wall
        # Active un bucle de cálculo de estrella
        for i in range(num):
            # Determine si se alcanza el punto final, determine si las coordenadas del nodo objetivo están en la lista de cierre
            tmp = self.in_close_list(self.target_node.x, self.target_node.y)
            if tmp:
                # Regresar a la ruta
                path_list = [[tmp.x, tmp.y]]
                # Ruta inversa
                while tmp.parent:
                    tmp = tmp.parent
                    path_list.append([tmp.x, tmp.y])
                # Lista inversa
                path_list.reverse()
                return True
            if not self.open_list:
                # Si open_list está vacío, no hay forma de ir
                return False
            # Seleccione el nodo de ruta mínima F de open_list
            minF = self.MinF()
            # Agregue el nodo seleccionado actualmente a close_list y elimínelo de open_list
            self.close_list.append(minF)
            self.open_list.remove(minF)
            # Busque la ruta y utilice el nodo actual como nodo principal para buscar de acuerdo con un orden fijo (fijo en la línea, en cualquier orden)
            self.search(AStar.Node(minF.x - 1, minF.y, minF))
            self.search(AStar.Node(minF.x, minF.y - 1, minF))
            self.search(AStar.Node(minF.x + 1, minF.y, minF))
            self.search(AStar.Node(minF.x, minF.y + 1, minF))
        else:
            return True


class Game(object):
    '' 'Juegos' ''

    def __init__(self, map2D, obs_num=None):
        'Inicialización'
        'Args:'
        '                  mapa 2D mapa 2D'
        '                  obs_num inicializa el número de obstáculos'
        
        self.map = map2D
        self.height = self.map.height
        self.width = self.map.width
        # Una dirección de movimiento inicial aleatoria
        self.direction = randint(0, 3)
        # Calcular el número de obstáculos de acuerdo con el tamaño del mapa
        # self.obs_num = int(math.sqrt(self.height * self.width))
        self.obs_num = obs_num if obs_num else int(
            math.sqrt(self.height * self.width))
        # Punto de inicio de inicialización
        self.current = [
            randint(int(1/4 * (self.height - 1)),
                    int(3/4 * (self.height - 1))),
            randint(int(1/4 * (self.width - 1)),
                    int(3/4 * (self.width - 1)))
        ]
        # Generar objetivo de fruta
        self.gen_fruit()
        # Generar obstáculos
        self.gen_obs()

    def gen_fruit(self):
        '' 'Generar fruta' ''
        while True:
            # Genera aleatoriamente coordenadas de fruta
            self.fruit = [randint(0, self.height - 1),
                          randint(0, self.width - 1)]
            # Evite la coincidencia de la fruta y las coordenadas del punto de partida
            if self.fruit != self.current:
                break

    def gen_obs(self):
        '' 'Generar obstáculos' ''
        self.obs_list = []
        for i in range(self.obs_num):
            while True:
                tmp = [randint(0, self.height - 1), randint(0, self.width - 1)]
                # Evite la superposición de obstáculos y puntos de partida o frutas
                if tmp != self.current and tmp != self.fruit:
                    self.obs_list.append(tmp)
                    break

    def move(self):
        'Moverse según la dirección de movimiento'
        '0, 1, 2, 3 corresponden a arriba, izquierda, abajo, derecha' 
      
        if self.direction == 0:
            self.current = [self.current[0] - 1, self.current[1]]
        elif self.direction == 1:
            self.current = [self.current[0], self.current[1] - 1]
        elif self.direction == 2:
            self.current = [self.current[0] + 1, self.current[1]]
        else:
            self.current = [self.current[0], self.current[1] + 1]

    def cls(self):
        '' 'Salida de consola vacía' ''
        os.system('cls')

    def load(self):
        '' 'Cargar frutas y obstáculos' ''
        # Cargar obstáculos
        for row, col in self.obs_list:
            self.map[row][col] = wall_char
        # Carga de fruta y punto actual
        row, col = self.current
        self.map[row][col] = self_char
        row, col = self.fruit
        self.map[row][col] = fruit_char

    def start(self):
        '' 'Iniciar juego en bucle' ''
        # Enciende una estrella
        g = self.a_star()
        # Entra en el bucle
        while True:
            # Borrar salida de consola
            self.cls()
            # Carga
            self.load()
            # Pantalla de impresión
            self.map.show()
            # Determine si ha comido la fruta
            if self.current == self.fruit:
                # Comer fruta
                # Restablecer mapa
                self.map.reload()
                # Regenerar fruta, regenerar obstáculos
                self.gen_fruit()
                self.gen_obs()
                self.map.reload()
            if next(g) is False:
                # No significa a dónde ir
                # Restablecer mapa
                self.map.reload()
                continue
            # Moverse
            self.move()
            # Control de velocidad de movimiento
            time.sleep(0.3)

    def a_star(self):
        '' 'Acceso al algoritmo A * para encontrar rutas'''
        '  Usa el generador de pitón para cambiar la dirección una vez en el ciclo del juego'
        
        # Crear objeto
        a = AStar(self.map)
        while True:
            # Cargue el mapa de visualización por adelantado, la visualización avanzada puede juzgar manualmente si realmente no hay camino a seguir
            # Borrar salida de consola
            self.cls()
            # Carga
            self.load()
            # Pantalla de impresión
            self.map.show()
            # Primer juicio inverso, si no hay forma de hacerlo en el número limitado de veces, agregue una estrategia de cambio hasta cierto punto para reducir el cálculo del tiempo de cálculo largo
            if a.sub_start(self.fruit, self.current, self.obs_list, 30) is False:
                # No significa a dónde ir
                input('No hay manera de ir, presione Entrar para actualizar el mapa')
                self.map.reload()
                self.gen_fruit()
                self.gen_obs()
                # No devuelve ninguna señal para ir
                yield False
                continue
            path_list = a.start(self.current, self.fruit, self.obs_list)
            if not path_list:
                # No significa a dónde ir
                # Cargue el mapa de visualización por adelantado, la visualización avanzada puede juzgar manualmente si realmente no hay camino a seguir
                # Borrar salida de consola
                # self.cls()
                # # Cargando
                # self.load()
                # # Imprimir pantalla
                # self.map.show()
                input('No hay manera de ir, presione Entrar para actualizar el mapa')
                self.map.reload()
                self.gen_fruit()
                self.gen_obs()
                # No devuelve ninguna señal para ir
                yield False
                continue
            # Recorre el camino después de comenzar, compara y obtén la dirección para caminar
            for path in path_list[1:]:
                if path[0] > self.current[0]:
                    self.direction = 2
                elif path[0] < self.current[0]:
                    self.direction = 0
                elif path[1] > self.current[1]:
                    self.direction = 3
                else:
                    self.direction = 1
                yield


if __name__ == "__main__":
    # Inicializa el tamaño de la consola
    os.system("mode con cols=80 lines=80")
    # Crear mapa
    map2D = Map2D(width=20, height=20)
    # Nuevo juego, especifica obstáculos
    game = Game(map2D, 150)
    # Comienza el juego
    game.start()
