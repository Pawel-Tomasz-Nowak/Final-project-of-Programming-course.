import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Zadeklaruj szerokość i wysokość okna.
width = 1900
height = 1080

window_size = (width, height)

background_color = (255, 255, 255)  # Biały kolor tła

# Stworzenie okna. Ten obiekt jest ważny, ponieważ jest on klasy Surface, czyli powierzchni, na którą można dodawać figury.
screen = pygame.display.set_mode(window_size)

pygame.display.set_caption("Moja Gra")  # Tytuł okna

# Wypełnienie tła
screen.fill(background_color)


# Pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Tutaj umieść kod rysujący elementy gry
    
    # Aktualizacja ekranu
    pygame.display.flip()
    





# Zakończenie Pygame
pygame.quit()
sys.exit()
