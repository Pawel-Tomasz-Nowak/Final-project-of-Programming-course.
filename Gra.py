import pygame as pg
from typing import Tuple, List
import sys
import Klasy


# Kolory
Color = Tuple[int, int, int]
WHITE: Color = (255, 255, 255)
MEDIUM_GRAY: Color = (100, 100, 100)
ORANGE: Color = (255, 131, 32)
BLACK: Color = (0, 0, 0)

# Zadeklaruj szerokość i wysokość okna.
screen_width: int = 400
screen_height: int = 750
window_size: tuple[int, int] = (screen_width, screen_height)


## ------------------------  SEKCJA DOTYCZĄCA EKRANU STARTOWEGO ------------------------
# Inicjalizacja Pygame
pg.init()

# Stworzenie okna. Ten obiekt jest ważny, ponieważ jest on klasy Surface, czyli powierzchni, na którą można dodawać figury.
intro_screen: pg.Surface = pg.display.set_mode(window_size)
font: pg.font.Font = pg.font.SysFont('Arial', 64)
small_font: pg.font.Font = pg.font.SysFont('Arial', 28)
mini_font: pg.font.Font = pg.font.SysFont('Arial', 18)

pg.display.set_caption("Moja Gra")   # Tytuł okna



def pokaz_ekran_startowy():
    start: bool = True
    tytul_text: pg.Surface = font.render("Nazwa gry", True, WHITE)
    graj_text: pg.Surface = font.render("GRAJ", True, WHITE)
    graj_rect: pg.Rect = graj_text.get_rect(center=(screen_width // 2, screen_height // 2))
    polecenie_text: pg.Surface = small_font.render("Kliknij GRAJ aby rozpocząć grę", True, MEDIUM_GRAY)
    polecenie_rect: pg.Rect = polecenie_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    instrukcja_lines: List[str] = [
        "Ustaw armatę pod odpowiednim kątem.",
        "Wystrzel piłkę klikając lewy przycisk myszy.",
        "Pamiętaj, że piłka może odbić się tylko dwa razy!",
        "Powodzenia!"
    ]

    instrukcja_texts: List[pg.Surface] = [mini_font.render(line, True, BLACK) for line in instrukcja_lines]
    instrukcja_rects: List[pg.Rect] = [instrukcja_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200 + i * 30)) for i, instrukcja_text in enumerate(instrukcja_texts)]

    while start:
        for zdarzenie in pg.event.get():
            if zdarzenie.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif zdarzenie.type == pg.MOUSEBUTTONDOWN:
                if zdarzenie.button == 1 and graj_rect.collidepoint(zdarzenie.pos):
                    start = False

        intro_screen.fill(ORANGE)
        intro_screen.blit(tytul_text, (screen_width // 2 - tytul_text.get_width() // 2, 150))
        intro_screen.blit(graj_text, graj_rect)

        intro_screen.blit(polecenie_text, polecenie_rect)
        for instrukcja_text, instrukcja_rect in zip(instrukcja_texts, instrukcja_rects):
            intro_screen.blit(instrukcja_text, instrukcja_rect)

        pg.display.update()

pokaz_ekran_startowy()




# # ------------------------ SEKCJA GŁÓWNA GRY ------------------------
screen: pg.Surface = pg.display.set_mode(window_size)
running = True

screen.fill(color = ORANGE, )

#stworzenie tablicy
tablica_kolor = (255,255,255)
tablica_wysokość = 100
tablica_szerokość = 150
kosz_kolor = (255,0,0)
kosz_wysokość = 60
kosz_szerokość = 80


tablica = pg.Rect(screen_width//2 - tablica_szerokość//2, screen_height*1//5-tablica_wysokość//2, tablica_szerokość, tablica_wysokość)
kosz = pg.Rect(screen_width//2 - kosz_szerokość//2, screen_height*1//5+tablica_wysokość//2-kosz_wysokość, kosz_szerokość, kosz_wysokość)
pg.draw.rect(screen, tablica_kolor, tablica)
pg.draw.rect(screen, kosz_kolor, kosz)

#Narysuj pierwszą armatę wypionizowaną.
Działo =Klasy.Cannon(window_size[0]/2, window_size[1]-125, 50, 100,)
Działo.NarysujArmatę(surface = screen, color = [0, 0,0])


#Zmienna mówiąca, czy kula zostala wystrzelona.
shot_ball: bool = False



while running:
        Działo.NarysujArmatę(surface = screen, color = ORANGE)

        #Tworzenie nowego działa.
        Działo = Klasy.Cannon(window_size[0]/2, window_size[1]-125, 50, 100)

        kat =  Klasy.Cannon.PoliczKąt(Działo.x0, Działo.y0)
                    
        if kat is not False:
            Działo.slope = kat

        Działo.NarysujArmatę(surface = screen, color = [0,0,0])

                
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if shot_ball is False:
                        Kula = Działo.WystrzelKulę(screen = screen, speed = 0.5)


                        shot_ball = True
                    

        if shot_ball is True:
            #Skasuj poprzednią wersję kulki.
            Kula.NarysujKule(screen, color = ORANGE)

            Kula.AktualizujWspółrzędne()

            Kula.NarysujKule(screen  = screen)

            #Sprawdzanie, czy kula nie wyszła poza mapę.
            if Kula.x < Kula.r or Kula.x > window_size[0]-Kula.r:
                Kula.dx = -Kula.dx
                #Zwiększ liczbę odbić o jeden.
                Kula.n_odbic += 1

            
            if Kula.y <= Kula.r or Kula.n_odbic == 3:
                #Wymaż kulkę
                Kula.NarysujKule(screen, color = ORANGE)
                shot_ball = False
           


        pg.display.update()


