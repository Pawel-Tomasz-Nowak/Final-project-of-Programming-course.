import pygame as pg
import sys

# Inicjalizacja Pygame
pg.init()
# Zadeklaruj szerokość i wysokość okna.
screen_width:int = 400
screen_height:int = 700

window_size = (screen_width, screen_height)

background_color = (255, 255, 255)  # Biały kolor tła

# Stworzenie okna. Ten obiekt jest ważny, ponieważ jest on klasy Surface, czyli powierzchni, na którą można dodawać figury.
screen:pg.Surface = pg.display.set_mode(window_size)

pg.display.set_caption("Moja Gra")  # Tytuł okna

# Wypełnienie tła
screen.fill(background_color)


# Pętla gry
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    # Tutaj umieść kod rysujący elementy gry
    
    # Aktualizacja ekranu
    pg.display.flip()
    





# Zakończenie Pygame
pg.quit()
sys.exit()
