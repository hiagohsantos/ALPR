import pygame
from time import sleep
import sys
import os

class SplashScreen:
    def __init__(self):
        pygame.init()
        self.fill_collor = (34, 34, 34)
        self.text_color = (182, 188, 194)
        self.screen_size = (250, 150)
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        x_pos = (screen_width - self.screen_size[0]) // 2
        y_pos = (screen_height - self.screen_size[1]) // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_pos},{y_pos}"
        pygame.display.set_caption('ALPR')
       
        self.screen = pygame.display.set_mode(self.screen_size, pygame.NOFRAME)
        #self.splash_image = pygame.image.load('caminho/para/sua/imagem/splash.png')
        self.screen.fill(self.fill_collor)
        self.font = pygame.font.Font(None, 20)
        
    def show_text(self, text):
        self.screen.fill(self.fill_collor)
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 - 20))
        #self.screen.blit(self.splash_image, (0, 0))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def show_progress_bar(self, progress):
        bar_width = 200
        bar_height = 5
        bar_x = (self.screen_size[0] - bar_width) // 2
        bar_y = self.screen_size[1] // 2
        
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (200, 200, 200), background_rect)

        bar_rect_width = bar_width * progress // 100
        bar_rect = pygame.Rect(bar_x, bar_y, bar_rect_width, bar_height)

        pygame.draw.rect(self.screen, (28, 114, 176), bar_rect)

        pygame.display.flip()


    def update(self, new_text, progress):
        self.show_text(new_text)
        self.show_progress_bar(progress)

    def close(self):
        pygame.quit()

if __name__ == "__main__":
    splash = SplashScreen()
    splash.update("opa", 10)
    sleep(1)
    splash.update("AEE", 20)
    sleep(1)
     
    splash.update("AEE", 30)
    sleep(1)
    splash.update("AEE", 40)
    sleep(1)
    splash.update("AEE", 50)
    sleep(1)
    splash.update("Concluído!", 100)
    sleep(1)