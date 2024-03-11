import pygame
import sys
import os

def show_splash_screen():
    pygame.init()
    screen_size = (300, 500)
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    x_pos = (screen_width - screen_size[0]) // 2
    y_pos = (screen_height - screen_size[1]) // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_pos},{y_pos}"

    
    screen = pygame.display.set_mode(screen_size, pygame.NOFRAME)
    pygame.display.set_caption('Splash Screen')

    # Carregue a imagem da splash screen
    splash_image = pygame.image.load('/home/pi/Desktop/ALPR/assets/images/splash1.jpg')

    # Crie um objeto de fonte para o texto
    font = pygame.font.Font(None, 36)

    # Crie um objeto de texto
    text = font.render('Seu Texto Aqui', True, (255, 255, 255))  # Cor branca

    # Posicione o texto no centro da tela
    text_rect = text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

    # Defina o tempo de exibição da splash screen (em milissegundos)
    display_time = 3000  # 3 segundos

    # Exiba a splash screen com o texto
    screen.blit(splash_image, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Aguarde o tempo de exibição da splash screen
    pygame.time.delay(display_time)

    # Feche a janela
    pygame.quit()

def main():
    show_splash_screen()

    # Adicione aqui o código principal do seu aplicativo

    # Exemplo: Aguarde alguns segundos antes de encerrar
    pygame.time.delay(2000)  # 2 segundos

    # Encerre o programa
    sys.exit()

if __name__ == "__main__":
    main()
