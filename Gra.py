import pygame as pg
import sys
import Klasy
from Stałe import screen_width, screen_height, window_size
from Stałe import ORANGE, WHITE, MEDIUM_GRAY, BLACK, LIGHT_BLUE
from Stałe import font, small_font, mini_font
from Stałe import end_button_width, end_button_height, end_button_color, end_button_text_color

#Inicjalizacja Pygame
pg.init()
## ------------------------  SEKCJA DOTYCZĄCA EKRANU STARTOWEGO ------------------------


def pokaz_ekran_startowy() -> None:
    """"Zadaniem tej funkcji jest stworzenie okna początkowego, które zawiera"""
    # Stworzenie okna. Ten obiekt jest ważny, ponieważ jest on klasy Surface, czyli powierzchni, na którą można dodawać figury.
    intro_screen: pg.Surface = pg.display.set_mode(window_size)
    pg.display.set_caption("Koszmata 3.0")   # Tytuł okna


    """"""
    running: bool = True
    tytul_text: pg.Surface = font.render("Koszmata 3.0", True, WHITE)
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

    while running:
        for zdarzenie in pg.event.get():
            if zdarzenie.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif zdarzenie.type == pg.MOUSEBUTTONDOWN:
                if zdarzenie.button == 1 and graj_rect.collidepoint(zdarzenie.pos):
                    running = False

        intro_screen.fill(ORANGE)
        intro_screen.blit(tytul_text, (screen_width // 2 - tytul_text.get_width() // 2, 150))
        intro_screen.blit(graj_text, graj_rect)

        intro_screen.blit(polecenie_text, polecenie_rect)
        for instrukcja_text, instrukcja_rect in zip(instrukcja_texts, instrukcja_rects):
            intro_screen.blit(instrukcja_text, instrukcja_rect)

        pg.display.update()

pokaz_ekran_startowy()


def draw_text(text:str, 
              font:pg.font.Font, color:tuple[int], 
              surface:pg.Surface, 
              x:float, y:float):
    
    """Ta funkcja rysuje tekst o treści 'text', którego czcionka jest określona przez argument font, a kolor jest określony
    przez parametr color. 
    Umiejscowienie tekstu jest zależne od pary (x,y). 
    Argument surface jest okienkiem, na którym chcemy wyrenderować tekst."""
    
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


#Ekran wyświetlany pod koniec gry.
def game_over_screen() -> bool:
    """"Funkcja ta zajmuje się wyświetlaniem ekranu końcowego, na którym wyświetlane są podstawowe
    statystyki, takie jak: dokładność nasza, liczba zdobytych przez nas punktów oraz czas gry. 
    Zwraca wartość bool równa True, jeżeli użytkownik chce zagrać ponownie , lub wartość False, gdy użytkownik ma dość gry."""
    global game_time, shots_attempted, shots_made
    

    #pg.time.get_ticks() zwraca wynik w milisekundach, więc zamień tę wartość na sekundy, dzieląc przez 1000.
    game_time = (pg.time.get_ticks() - czas_startu_gry)/1000
    end_button_rect = pg.Rect((window_size[0] - end_button_width) // 2, window_size[1] - 100, end_button_width, end_button_height)

    #Policz dokładnośc naszych strzałów, zaokrąglij ją.
    accuracy:float =  round((shots_made / shots_attempted) * 100,2)
    game_time_minutes:int = int(game_time // 60)
    game_time_seconds:int = int(game_time % 60)

    
    #Motornicza zmienna, utrzymująca program przy życiu.
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:

                #Jeżeli  kursor myszy znajduje się w przycisku resetującym grę, zresetuj grę.
                if end_button_rect.collidepoint(event.pos):
                    pokaz_ekran_startowy()

                    shots_attempted = 0
                    shots_made = 0
                    
                    return  True
         
            

        screen.fill(LIGHT_BLUE)

        # Rysowanie tekstu 'Koniec meczu'
        draw_text('Koniec meczu', font, BLACK, screen, screen_width // 2, screen_height // 4)

        # Rysowanie statystyk
        draw_text(f'Czas gry: {game_time_minutes}:{game_time_seconds:02d}', small_font, BLACK, screen, screen_width // 2, screen_height // 2 - 40)
        draw_text(f'Ilość punktów: {shots_made}', small_font, BLACK, screen, screen_width // 2, screen_height // 2)
        draw_text(f'Celność: {accuracy:.2f}%', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 40)

        # Rysowanie przycisku 'Zagraj ponownie'
        pg.draw.rect(screen, end_button_color, end_button_rect)
        draw_text('Zagraj ponownie', small_font, end_button_text_color, screen, end_button_rect.centerx, end_button_rect.centery)

        pg.display.flip()

    return False

# # ------------------------ SEKCJA GŁÓWNA GRY ------------------------

def NarysujEkranRozgrywki() -> tuple[pg.Surface, Klasy.Prostokąt, Klasy.Prostokąt]:
    """"Funkcja ta rysuje ekran, na którym ma miejsce główna rozgrywka.
    """
    #Stwórz ekran, na którym będzie pojawiać się piłka oraz armata  i inne atrakcje.
    screen: pg.Surface = pg.display.set_mode(window_size)


    screen.fill(color = ORANGE, )

    #Parametry tablicy.
    tablica_kolor = (255,255,255)
    tablica_wysokość = 100
    tablica_szerokość = 150


    #Parametry kosza.
    kosz_kolor = (255,0,0)
    kosz_wysokość = 60
    kosz_szerokość = 80

    #Stwórz obiekt klasy tablica i narysuj tę tablicę.
    tablica = Klasy.Prostokąt(anchor = (screen_width//2 - tablica_szerokość//2,screen_height*1//5-tablica_wysokość//2)
                            ,color = tablica_kolor, width = tablica_szerokość, height = tablica_wysokość
                            )
    
    tablica.NarysujProstokąt(screen = screen)


    #Stwórz obiekt klasy kosz i narysuj ten kosz.
    # UWAGA, Atrybut anchor obiektu kosz jest zależny od atrybutu anchor obiektu tablica. To należy uwzględnić po prototypie.
    kosz = Klasy.Prostokąt((screen_width//2 - kosz_szerokość//2,
                    screen_height*1//5+tablica_wysokość//2-kosz_wysokość), color = kosz_kolor, width = kosz_szerokość, 
                    height =  kosz_wysokość)

    kosz.NarysujProstokąt(screen = screen)

    return screen, tablica, kosz



screen, tablica, kosz  = NarysujEkranRozgrywki()

#Narysuj pierwszą armatę wypionizowaną.
Działo:Klasy.Cannon =Klasy.Cannon(window_size[0]/2, window_size[1]-125, 50, 100,)
Działo.NarysujArmatę(screen = screen, color = [0, 0,0])


# #Zmienne do statystyki z rozgrywki.
#Łączna liczba oddanych strzałów.
shots_attempted:int = 0
#Udane strzały.
shots_made:int = 0

#Czas gry
game_time:float = 0
#Maksymalna liczba dozwolonych strzałów
max_shots:int = 5


#Zmienna mówiąca, czy kula zostala wystrzelona.
shot_ball: bool = False


#Moment rozpoczęcia gry. Będzie ta zmienna ważna przy podsumowaniu statystyk.
czas_startu_gry = pg.time.get_ticks()

#Zmienna, która odpowiada za trwanie rozgrywki.
running:bool = True



while running:
        Działo.NarysujArmatę(screen = screen, color = ORANGE)


     
        #Tworzenie nowego działa.
        Działo = Klasy.Cannon(window_size[0]/2, window_size[1]-125, 50, 100)

        #Policz kąt nachylenia armaty.
        kąt =  Klasy.Cannon.PoliczKąt(Działo.x0, Działo.y0)
        
        #Jeżęli kąt nie jest równy False (czyli kąt nie jest równy 0 i nie jest równy pi), to zmień wartość kąta
        #Jeżęli kąt jest równy False, to kąt domyślnie jest równy pi/2, czyli armata jest wypionizowana.
        if kąt is not False:
            Działo.slope = kąt

        Działo.NarysujArmatę(screen = screen, color = [0,0,0])

                
        for event in pg.event.get():
            #Klasyczne wyjście z okienka rozgrywki, gdy klikniemy "X" w prawym górnym rogu.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            #Sprawdzamy, czy użytkownik nacisnął przycisk myszy.
            elif event.type == pg.MOUSEBUTTONDOWN:

                #A dokładniej - czy nacisnął lewy przycisk myszy
                if event.button == 1:
                    #Jeżeli w momencie strzału nie ma w obiegu kuli, wystrzel kulę.
                    if shot_ball is False:
                        Kula = Działo.WystrzelKulę(screen = screen, speed = 0.5)

                        #Ta zmienna shot_ball ustawi się ponownie na False, gdy kula (dotknię Tablicy lub obręczy) 
                        #lub gdy górny punkt piłki bedzie zbyt wysoko.
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

            #Jeżeli liczba wykonanych odbić przekroczy dwa, wymaż kulkę.
            if Kula.y <= Kula.r or Kula.n_odbic == 3:
                #Wymaż kulkę
                Kula.NarysujKule(screen, color = ORANGE)
                shot_ball = False

            Obszar_Obręcz = pg.Rect((kosz.anchor[0], kosz.anchor[1]+kosz.height), (kosz.width, 1))
            Obszar_Tablica = pg.Rect(( tablica.anchor[0], tablica.anchor[1]), (tablica.width, tablica.height))

            if Obszar_Obręcz.collidepoint(Kula.x, Kula.y):
                shots_made += 1

                Kula.NarysujKule(screen, color = ORANGE)

                shot_ball = False

            elif Obszar_Tablica.collidepoint(Kula.x, Kula.y):
                Kula.NarysujKule(screen = screen, color = ORANGE)

                shot_ball = False

            
        #Napraw kosz i tablicę.
        tablica.NarysujProstokąt(screen = screen)
        kosz.NarysujProstokąt(screen = screen)


        
        if shots_attempted >= max_shots and shot_ball == False:
        # Wyświetl ekran końcowy
            czy_kontynuować = game_over_screen()

            #Jeżeli gracz chce kontynuować grę, zresetuj grę.
            if czy_kontynuować == True:
                screen, tablica, kosz = NarysujEkranRozgrywki()

                czas_startu_gry = pg.time.get_ticks()

                shot_ball = False
            else:
                break

            
        pg.display.update()
