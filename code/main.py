import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # Inicialização do Pygame e configuração da tela
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('AEDventure')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        # Loop principal do jogo
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()
                    if event.key == pygame.K_e and not self.level.show_challenge:
                        self.level.start_challenge()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level.show_challenge and not self.level.sorting_challenge.is_active:
                        self.level.sorting_challenge.check_difficulty_selection(event)
                    else:
                        self.level.sorting_challenge.check_button_click(event)
                        self.level.pause_menu.check_mouse_click(event)

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    # Criação e execução do jogo
    game = Game()
    game.run()