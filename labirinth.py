from datetime import datetime
import random

class Labirinth:
    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.matriz = []
        self.L = []
        #verifica se ha uma saida
        self.isBorderFill = False
        #estado inicial (inicio da jornada do codibentinho)
        self.start = (0, 0)
        #estado final (fim do labirinto)
        self.end = (0, 0)

    def create_matriz(self):
        for _ in range(self.M):
            row = ['#'] * self.N
            self.matriz.append(row)

    def create_path(self, i, j):
        di = [0, 0, 1, -1]
        dj = [-1, 1, 0, 0]
        for k in range(len(di)):
            self.L.append((di[k] + i, dj[k] + j, di[k] * 2 + i, dj[k] * 2 + j))
            
# Funcao auxiliar para montar as coordenadas com base na tupla informada
    def get_coordinates(self, move):
        coordinates = {}
        coordinates['i1'] = move[0]
        coordinates['j1'] = move[1]
        coordinates['i2'] = move[2]
        coordinates['j2'] = move[3]
        return coordinates
# Retorna verdadeiro se a tupla com as coordenadas for uma parede
    def available_moves(self, move):
        pos = self.get_coordinates(move)
        if pos['i2'] >= 0 and pos['i2'] < self.M and pos['j2'] >= 0 and pos['j2'] < self.N:
            if self.is_border(pos['i2'], pos['j2']):
                if self.isBorderFill:
                    return False
                else:
                    self.isBorderFill = True
                    return self.isBorderFill
            return self.matriz[pos['i2']][pos['j2']] == '#'
        return False

    def is_possible_move(self, position):
        # Inicializa uma lista vazia para armazenar os movimentos válidas.
        moves = []  
        # Para cada combinação de movimentos possíveis nas direções: direita, esquerda, abaixo e acima.
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            # Calcula a nova posição somando as coordenadas atuais com as diferenças di e dj.
            new_position = (position[0] + di, position[1] + dj)
            # Verifica se a nova posição é válida (dentro dos limites do labirinto e não é uma parede).
            if self.is_valid(new_position):
                # Se a posição for válida, adiciona-a à lista de ações possíveis.
                moves.append(new_position)
        # Retorna a lista de posições válidas.
        return moves

    #Verifica se a posição desejada não é uma parede
    def is_valid(self, position):
        return (
            0 <= position[0] < self.M
            and 0 <= position[1] < self.N
            and self.matriz[position[0]][position[1]] != "#"
        )

    def random_init_path(self):
        ## Gera aleatoriamente a posicao inicial do codebentinho
        ## com as restricoes de ser ímpar entre x = [3, N-2] e y = [3, M-2]
        startX0 = 2 * random.randint(1, ((self.M - 1) // 2) - 1) + 1
        startY0 = 2 * random.randint(1, ((self.N - 1) // 2) - 1) + 1
  
        self.matriz[startX0][startY0] = 'C'
        self.start = (startX0, startY0)
        self.create_path(startX0, startY0)
        ##Gera labirinto de acordo com as instrucoes passada
        while len(self.L):
            randomPath = random.randint(0, len(self.L) - 1)
            randomMove = self.L[randomPath]
            del self.L[randomPath]
            if self.available_moves(randomMove):
                pos = self.get_coordinates(randomMove)
                self.matriz[pos['i1']][pos['j1']] = '.'
                if self.is_border(pos['i2'], pos['j2']):
                    self.matriz[pos['i2']][pos['j2']] = 'S'
                    self.end = (pos['i2'], pos['j2'])
                else:
                    self.matriz[pos['i2']][pos['j2']] = '.'
                self.create_path(pos['i2'], pos['j2'])
## Verifica se esta em uma borda
    def is_border(self, i, j):
        return i == 0 or i == self.M - 1 or j == 0 or j == self.N - 1
