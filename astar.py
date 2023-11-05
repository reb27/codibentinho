class Astar:
    def __init__(self, labirinth):
        self.labirinth = labirinth
        self.start = labirinth.start
        self.end = labirinth.end
        self.heap = []  # Fila de prioridades para reservar os estados de estados. (nossa Agenda)
        self.visited = set()  # Set para armazenar os estados visitados. (nossa EstadosPassados)
   
        self.path = {}  # Dicionário que armazena as coordenadas referentes ao caminho de saída

    # Calcula a distância de Manhattan entre duas posições.
    def heuristic(self, position):
        return abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])

    # Executa o algoritmo A* para encontrar o caminho no labirinto.
    def search(self):
        # Insere o estado inicial na fila de prioridade.
        self.insert_new_key_min_heap((0, self.start))

        # Inicia o caminho de saída com o estado inicial que nesse caso é None.
        self.path[self.start] = None

        # Enquanto a fila de prioridade não estiver vazia, continue a busca.
        while self.heap:
            # Seleciona o estado com o menor custo da fila de prioridade (que é uma heap minima)
            current = self.get_min_value()

            # Se o estado atual for o estado final, retorna o caminho construído até esse ponto.
            if current[1] == self.end:
                return self.make_path(current[1])

            # Se o estado atual já foi visitado, ele é ignorado.
            if current[1] in self.visited:
                continue

            self.visited.add(current[1])

            # Para cada posição vizinha válida, expande os estados e os adiciona à fila de prioridade.
            for next_position in self.labirinth.is_possible_move(current[1]):
                if next_position not in self.path:
                    self.path[next_position] = current[1]
                    new_cost = 1
                    priority = new_cost + self.heuristic(next_position)
                    self.insert_new_key_min_heap((priority, next_position))

        # Se a fila de prioridade esvaziar e o estado final não for encontrado, retorna None (sem solução).
        return None

    # Função responsável por pegar o menor valor presente na heap (por ser uma heap minima, será o primeiro elemento)
    def get_min_value(self):
        min_element = self.heap[0]
        last_element = self.heap.pop()
        if self.heap:
            self.heap[0] = last_element
            self.min_heapify(0)
        return min_element

    # Função para aumentar a chave na heap (min-heap) e manter a propriedade de min-heap.
    def increase_key_min_heap(self, pos, new_value):
        self.heap[pos] = new_value
        i = pos
        parent = (i - 1) // 2
        while i > 0 and self.heap[parent][0] > new_value[0]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2


    # Função para inserir uma nova chave na heap (min-heap).
    def insert_new_key_min_heap(self, key):
        self.heap.append(key)
        self.increase_key_min_heap(len(self.heap) - 1, key)

    def min_heapify(self, i):
        min_index = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(self.heap) and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right
        if min_index != i:
            self.heap[i], self.heap[min_index] = self.heap[min_index], self.heap[i]
            self.min_heapify(min_index)

    def make_path(self, current):
        path = []
        while current is not None:
            path.append(current)
            current = self.path[current]
        return path[::-1]
