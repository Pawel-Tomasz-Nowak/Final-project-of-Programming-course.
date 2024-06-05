import pygame as pg
import sys
import Klasy
from Stałe import screen_width, screen_height, window_size
from Stałe import ORANGE, WHITE, MEDIUM_GRAY, BLACK, LIGHT_BLUE
from Stałe import font, small_font, mini_font
from Stałe import end_button_width, end_button_height, end_button_color, end_button_text_color
from Stałe import tablica_kolor, tablica_szerokość, tablica_wysokość
from Stałe import kosz_kolor, kosz_szerokość, kosz_wysokość


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

        intro_screen.fill(ORANGE) #Wypełnij okno startowe na pomarańczowo
        intro_screen.blit(tytul_text, (screen_width // 2 - tytul_text.get_width() // 2, 150)) #Dodaj tytuł gry na powierzchnie.
        intro_screen.blit(graj_text, graj_rect) #Dodaj przycisk graj na powierzchnie

        intro_screen.blit(polecenie_text, polecenie_rect) #Dodaj okno z zachętą do rozpoczęcia gry.
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
    global game_time, shots_attempted, shots_scored
    

    #pg.time.get_ticks() zwraca wynik w milisekundach, więc zamień tę wartość na sekundy, dzieląc przez 1000.
    game_time = (pg.time.get_ticks() - czas_startu_gry)/1000
    end_button_rect = pg.Rect((window_size[0] - end_button_width) // 2, window_size[1] - 100, end_button_width, end_button_height)

    #Policz dokładnośc naszych strzałów, zaokrąglij ją.
    accuracy:float =  round((shots_scored / shots_attempted) * 100,2)
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
                    pokaz_ekran_startowy() #Wracamy do okienka początkowego.

                    shots_attempted = 0 #Wyzeruj wszystkie statystyki związane z liczbą punktów.
                    shots_scored = 0
                    
                    return  True #Zwrócenie True przyda się w dolnych partiach kodu. Będzie oznaczało, że chcemy grać dalej.
         
            

        game_screen.fill(LIGHT_BLUE)

        # Rysowanie tekstu 'Koniec meczu'
        draw_text('Koniec meczu', font, BLACK, game_screen, screen_width // 2, screen_height // 4)

        # Rysowanie statystyk
        draw_text(f'Czas gry: {game_time_minutes}:{game_time_seconds:02d}', small_font, BLACK, game_screen, screen_width // 2, screen_height // 2 - 40)
        draw_text(f'Ilość punktów: {shots_scored}', small_font, BLACK, game_screen, screen_width // 2, screen_height // 2)
        draw_text(f'Celność: {accuracy:.2f}%', small_font, BLACK, game_screen, screen_width // 2, screen_height // 2 + 40)

        # Rysowanie przycisku 'Zagraj ponownie'
        pg.draw.rect(game_screen, end_button_color, end_button_rect)
        draw_text('Zagraj ponownie', small_font, end_button_text_color, game_screen, end_button_rect.centerx, end_button_rect.centery)

        pg.display.flip()

    return False

# # ------------------------ SEKCJA GŁÓWNA GRY ------------------------

def NarysujEkranRozgrywki() -> tuple[pg.Surface, Klasy.Prostokąt, Klasy.Prostokąt]:
    """"Funkcja ta rysuje ekran, na którym ma miejsce główna rozgrywka.
    """
    #Stwórz ekran, na którym będzie pojawiać się piłka oraz armata  i inne atrakcje.
    screen: pg.Surface = pg.display.set_mode(window_size)


    screen.fill(color = ORANGE, )





    tablica = Klasy.Prostokąt(anchor = (screen_width//2 - tablica_szerokość//2,screen_height*1//5-tablica_wysokość//2)
                            ,color = tablica_kolor, width = tablica_szerokość, height = tablica_wysokość
                            ) #Stwórz obiekt klasy Prostokąt, który będzie reprezentował tablicę.
    
    tablica.NarysujProstokąt(screen = screen) #Narysuj tę tablicę.


  
    kosz = Klasy.Prostokąt(anchor = (screen_width//2 - kosz_szerokość//2,screen_height*1//5+tablica_wysokość//2-kosz_wysokość), 
                           color = kosz_kolor, width = kosz_szerokość, 
                    height =  kosz_wysokość) #Stwórz obiekt klasy prostokąt, który będzie reprezentował obręcz.
                                            #Uwaga, Atrybut anchor będzie zależny od atrybutu anchor obiektu tablica. Ma to znaczenie, gdy tablica będzie się ruszała
    

    kosz.NarysujProstokąt(screen = screen) #Rysowanie obręczy (inaczej nazywany koszem)

    return screen, tablica, kosz



#game_screen jest okienkiem, na którym rysujemy obiekty będącę interaktywnymi elementami rozgrywki.
#tablica reprezentuje cały obiekt, na którym zawiszony jest kosz.
#kosz jest z kolei celem, w którego trafienie jest najważniejszym zadaniem gry.
game_screen, tablica, kosz  = NarysujEkranRozgrywki()


Działo:Klasy.Cannon =Klasy.Cannon(x0 = window_size[0]/2, y0=window_size[1]-125, #Po naciśnieciu przycisku start stwórz armatę
                                  width = 50,  height = 100,) #która domyślnie jest wypionizowana (tj. jej nachylenie wynosi 90 stopni)

Działo.NarysujArmatę(screen = game_screen, color = [0, 0,0]) #Teraz narysuj tę armatę.




#Poniższe cztery zmienne będą wykorzystywane do statystyk.
shots_attempted:int = 0  #Liczba oddanych strzałów (celnych lub niecelnych)
shots_scored:int = 0 #Celne strzały.
game_time:float = 0 #Czas trwania gry (od momentu nacisnięcia przycisku "GRAJ")
max_shots:int = 5 #Maksdymalna liczba dozwolonych strzałów. Po przekroczeniu jej, ekran rozgrywki przechodzi do ekranu końcowego.


#Zmienna mówiąca, czy kula zostala wystrzelona.
shot_ball: bool = False


#Moment rozpoczęcia gry. Będzie ta zmienna ważna przy podsumowaniu statystyk.
czas_startu_gry = pg.time.get_ticks()

#Zmienna, która odpowiada za trwanie rozgrywki.
running:bool = True



while running:
        Działo.NarysujArmatę(screen = game_screen, color = ORANGE)


     
        #Tworzenie nowego działa.
        Działo = Klasy.Cannon(window_size[0]/2, window_size[1]-125, 50, 100)

        #Policz kąt nachylenia armaty.
        kąt =  Klasy.Cannon.PoliczKąt(Działo.x0, Działo.y0)
        
        #Jeżęli kąt nie jest równy False (czyli kąt nie jest równy 0 i nie jest równy pi), to zmień wartość kąta
        #Jeżęli kąt jest równy False, to kąt domyślnie jest równy pi/2, czyli armata jest wypionizowana.
        if kąt is not False:
            Działo.slope = kąt

        Działo.NarysujArmatę(screen = game_screen, color = [0,0,0])

                
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
                        Kula = Działo.WystrzelKulę(screen = game_screen, speed = 0.5)

                        #Ta zmienna shot_ball ustawi się ponownie na False, gdy kula (dotknię Tablicy lub obręczy) 
                        #lub gdy górny punkt piłki bedzie zbyt wysoko.
                        shot_ball = True

                        shots_attempted += 1

            
       
        if shot_ball is True:
            #Skasuj poprzednią wersję kuli.
            Kula.NarysujKule(screen = game_screen, color = ORANGE)
    
            #Aktualizacja współrzędnych środka kuli.
            Kula.AktualizujWspółrzędne()

            #Narysuj kule na nowo.
            Kula.NarysujKule(screen  = game_screen)

            #Jeżeli kulka odbija się od pionowych krawędzi ekranu, zmień składową poziomą wektora prędkości na przeciwną.
            if Kula.x < Kula.r or Kula.x > window_size[0]-Kula.r:
                Kula.dx = -Kula.dx
                #Zwiększ liczbę odbić o jeden.
                Kula.n_odbic += 1

            #Jeżeli (środek kulki znajdzie się w odległości mniejszej niż promień kuli od poziomej krawędzi 
            #lub jeżeli kulka odbije się co najmniej trzy razy), wtedy wymaż kulę.
            if Kula.y <= Kula.r or Kula.n_odbic == 3:
                #Wymaż kulkę
                Kula.NarysujKule(screen = game_screen, color = ORANGE)
                shot_ball = False

            #Znajdź obszary prostokątne, które reprezentują odpowiędnio obręcz (inaczej kosz)  oraz tablicę.
            Obszar_Obręcz = pg.Rect((kosz.anchor[0], kosz.anchor[1]+kosz.height), (kosz.width, 1))
            Obszar_Tablica = pg.Rect(( tablica.anchor[0], tablica.anchor[1]), (tablica.width, tablica.height))

            #Jeżeli środek kuli znajduje się w obszarze obręczy (tj. obszar aktywacyjny (trigger area)), to naliczamy punkt.
            if Obszar_Obręcz.collidepoint(Kula.x, Kula.y):
                shots_scored += 1
                shot_ball = False

            elif Obszar_Tablica.collidepoint(Kula.x, Kula.y):
        
                shot_ball = False

            
        #Napraw kosz i tablicę.
        tablica.NarysujProstokąt(screen = game_screen)
        kosz.NarysujProstokąt(screen = game_screen)


        
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
