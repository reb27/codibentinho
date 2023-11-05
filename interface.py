from astar import Astar

import pygame

class Interface:
    def __init__(self, labirinth, N, M, path):
        pygame.init()
        self.labirinth = labirinth
        self.N = N
        self.resolving = False 
        self.M = M
        self.size = 30
        self.path = path
        self.current_pos = labirinth.start
        self.end = labirinth.end
        self.start = labirinth.start
        self.current_path = [] 
        self.not_moving = True
        self.block = pygame.image.load('./assets/bloco.png')
        self.grass = pygame.image.load('./assets/grama.jpg')
        self.codibentinho = pygame.image.load('./assets/codibentinho.png')
        self.yellow_color = (255, 255, 0) 
        self.background_color = (125, 201, 48)

        self.screen = pygame.display.set_mode((N * 30, M * 45))
        pygame.display.set_caption("Labirinth")
        self.font = pygame.font.Font(None, 36)

    def draw_labirinth(self):
        for i in range(self.M):
            for j in range(self.N):
                if (i, j) != self.end:
                    if (i, j) != self.current_pos: 
                        if self.start == (i, j):
                           self.screen.blit(pygame.transform.scale(self.grass, (self.size, self.size)), (j * self.size, i * self.size))
                        else:
                            self.screen.blit(pygame.transform.scale(self.block, (self.size, self.size)), (j * self.size, i * self.size))
                if self.labirinth.matriz[i][j] == '.':
                    self.screen.blit(pygame.transform.scale(self.grass, (self.size, self.size)), (j * self.size, i * self.size))
        pygame.draw.rect(self.screen, self.yellow_color, [self.end[1] * self.size, self.end[0] * self.size, self.size, self.size])


    def draw_path(self):
        for position in self.current_path:
            i, j = position
            pygame.draw.rect(self.screen, (0, 255, 0), [j * self.size, i * self.size, self.size, self.size])

    def draw_menu(self):
        title_color = (125,201,48)
        description_color = (200, 200, 200) 
        background_color =(84,140,12)
        title_font = pygame.font.Font(None, 36)

        menu_text = [
            ("Pressione as teclas:", title_color),
            ("Seta para a esquerda: Mova para a esquerda", description_color),
            ("Seta para a direita: Mova para a direita", description_color),
            ("Seta para cima: Mova para cima", description_color),
            ("Seta para baixo: Mova para baixo", description_color),
            ("R: Resolver a partir da posição atual", description_color)
        ]

        menu_y = self.M * 30 + 15

        menu_height = len(menu_text) * 35
        pygame.draw.rect(self.screen, background_color, (0, menu_y, self.N * 30, menu_height),border_radius=40)

        for line, color in menu_text:
            text = title_font.render(line, True, color if line == menu_text[0][0] else description_color)
            text_rect = text.get_rect(center=(self.N * 30 // 2, menu_y + 18))
            self.screen.blit(text, text_rect)
            menu_y += 30


    def process_key_events(self, event):
        directions = { pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1), pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0)}

        if event.key in directions:
            new_pos = (self.current_pos[0] + directions[event.key][0], 
                       self.current_pos[1] + directions[event.key][1])
            if self.labirinth.is_valid(new_pos):
                self.current_pos = new_pos
                self.resolving = False
                
        elif event.key == pygame.K_r:
            self.resolving = True
            
        
    def resolve(self):
        astar = Astar(self.labirinth)
        astar.start = self.current_pos
        current_path = astar.search()
        if current_path:
            self.current_path = current_path
            self.draw_path()

    def run(self):
        running = True
        show_codibentinho = True  

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.process_key_events(event)

            if self.resolving:
                self.resolve()
                #resolve o loop infinito
                self.resolving = False
            
            self.screen.fill(self.background_color)

            self.draw_labirinth()
            self.draw_path()
            self.draw_menu()

            if show_codibentinho:
                self.screen.blit(pygame.transform.scale(self.codibentinho, (30, 30)),[self.current_pos[1] * 30, self.current_pos[0] * 30, 30, 30])

            pygame.display.flip()

        pygame.quit()