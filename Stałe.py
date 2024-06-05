from typing import Tuple
import pygame as pg

pg.init()

# Kolory
Color = Tuple[int, int, int]
WHITE: Color = (255, 255, 255)
MEDIUM_GRAY: Color = (100, 100, 100)
ORANGE: Color = (255, 131, 32)
BLACK: Color = (0, 0, 0)
LIGHT_BLUE: Color = (173, 216, 230)


# Zadeklaruj szerokość i wysokość okna.
screen_width: int = 400
screen_height: int = 750
window_size: tuple[int, int] = (screen_width, screen_height)


# Rozmiary czcionek.
font: pg.font.Font = pg.font.SysFont('Arial', 64)
small_font: pg.font.Font = pg.font.SysFont('Arial', 28)
mini_font: pg.font.Font = pg.font.SysFont('Arial', 18)


# Parametry przycisku 'Zagraj ponownie'
end_button_width = 200
end_button_height = 50
end_button_color = ORANGE
end_button_text_color = WHITE

#Parametry tablicy.
tablica_kolor = (255,255,255)
tablica_wysokość = 100
tablica_szerokość = 150


#Parametry kosza.
kosz_kolor = (255,0,0) #Kolor kosza w kodowaniu RGB
kosz_wysokość = 60 #Wysokość kosza
kosz_szerokość = 80 #Szerokość kosza
