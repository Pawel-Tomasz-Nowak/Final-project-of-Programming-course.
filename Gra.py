import pygame as pg
import sys
import Klasy
from Stałe import screen_width, screen_height, window_size, ORANGE, WHITE, MEDIUM_GRAY, BLACK, LIGHT_BLUE

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
    instrukcja_lines: list[str] = [
        "Ustaw armatę pod odpowiednim kątem.",
        "Wystrzel piłkę klikając lewy przycisk myszy.",
        "Pamiętaj, że piłka może odbić się tylko dwa razy!",
        "Powodzenia!"
    ]

    instrukcja_texts: list[pg.Surface] = [mini_font.render(line, True, BLACK) for line in instrukcja_lines]
    instrukcja_rects: list[pg.Rect] = [instrukcja_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200 + i * 30)) for i, instrukcja_text in enumerate(instrukcja_texts)]

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


#ekran koncowy

# Przycisk 'Zagraj ponownie'
button_width = 200
button_height = 50
button_color = ORANGE
button_text_color = WHITE
button_rect = pg.Rect((window_size[0] - button_width) // 2, window_size[1] - 100, button_width, button_height)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def reset_game():
    global shots_attempted    #shots_made, points, game_time
    shots_attempted = 0
    # shots_made = 0
    # points = 0
    # game_time = 0

def game_over_screen():
    # global game_time, points, shots_attempted, shots_made
    # accuracy = (shots_made / shots_attempted) * 100 if shots_attempted > 0 else 0
    # game_time_minutes = game_time // 60
    # game_time_seconds = game_time % 60
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pokaz_ekran_startowy()
                    reset_game()
                    return True

        screen.fill(LIGHT_BLUE)

        # Rysowanie tekstu 'Koniec meczu'
        draw_text('Koniec meczu', font, BLACK, screen, screen_width // 2, screen_height // 4)

        # Rysowanie statystyk
        # draw_text(f'Czas gry: {game_time_minutes}:{game_time_seconds:02d}', small_font, BLACK, screen, screen_width // 2, screen_height // 2 - 40)
        # draw_text(f'Ilość punktów: {points}', small_font, BLACK, screen, screen_width // 2, screen_height // 2)
        # draw_text(f'Celność: {accuracy:.2f}%', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 40)

        # Rysowanie przycisku 'Zagraj ponownie'
        pg.draw.rect(screen, button_color, button_rect)
        draw_text('Zagraj ponownie', small_font, button_text_color, screen, button_rect.centerx, button_rect.centery)

        pg.display.flip()


# # ------------------------ SEKCJA GŁÓWNA GRY ------------------------
screen: pg.Surface = pg.display.set_mode(window_size)
running = True

screen.fill(color = ORANGE, )

# #Zmienne do statystyki z rozgrywki (odkodowanie = ctrl + "/")
shots_attempted = 0
# shots_made = 0
# points = 0
# game_time = 0
max_shots = 20

#Parametry tablicy.
tablica_kolor = (255,255,255)
tablica_wysokość = 100
tablica_szerokość = 150


#Parametry kosza.
kosz_kolor = (255,0,0)
kosz_wysokość = 60
kosz_szerokość = 80


tablica = Klasy.Prostokąt(anchor = (screen_width//2 - tablica_szerokość//2,screen_height*1//5-tablica_wysokość//2)
                          ,color = tablica_kolor, width = tablica_szerokość, height = tablica_wysokość
                          )
tablica.NarysujProstokąt(screen = screen)



kosz = Klasy.Prostokąt((screen_width//2 - kosz_szerokość//2,
                screen_height*1//5+tablica_wysokość//2-kosz_wysokość), color = kosz_kolor, width = kosz_szerokość, 
                 height =  kosz_wysokość)

kosz.NarysujProstokąt(screen = screen)




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
                        shots_attempted += 1
                    

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

        #Napraw kosz i tablicę.
        tablica.NarysujProstokąt(screen = screen)
        kosz.NarysujProstokąt(screen = screen)

        if shots_attempted >= max_shots:
        # Wyświetl ekran końcowy
            game_over_screen()
            


        pg.display.update()

#Aktualny problem to ze nie ma mozliwsci zdefiniowac zmiennych jak skutecznosci, zdobyty punkt itd., 
#oraz fakt ze po nacisnieciu zagraj ponownie przenosi nas na ekran startowy gdzie po nacisnieciu start
#gra sie zaczyna ale toczy sie na ekranie startowym a nie na ekranie na ktorym powinna sie odbywac gra  
