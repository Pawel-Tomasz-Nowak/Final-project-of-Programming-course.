import pygame as pg #Główny moduł
import sys
import Klasy #Moduł zawierający wszystkie klase wykorzystywane w grze.
from Stałe import screen_width, screen_height, window_size
from Stałe import ORANGE, WHITE, MEDIUM_GRAY, BLACK, LIGHT_BLUE
from Stałe import font, small_font, mini_font
from Stałe import end_button_width, end_button_height, end_button_color, end_button_text_color
from Stałe import tablica_kolor, tablica_szerokość, tablica_wysokość
from Stałe import kosz_kolor, kosz_szerokość, kosz_wysokość, k
import pathlib as path #Przyda nam się do uzyskiwania ścieżki do folderu z tłami.


#Zainicjuj mikser dźwieku
pg.mixer.init()

#Wczytaj dźwięk eksplozji.
explosion_sound = pg.mixer.Sound(file = path.Path(r"Dzwieki")/"Dźwięk wystrzału.mp3")
#Wczytaj jingiel końcowy
ending_theme = pg.mixer.Sound(file = path.Path(r"Dzwieki")/"Jingiel końcowy.mp3")
#Wczytaj dźwięk trafienia.
scoring_theme = pg.mixer.Sound(file =path.Path(r"Dzwieki")/"ScoringSound.mp3")


#Inicjalizacja Pygame
pg.init()
## ------------------------  SEKCJA DOTYCZĄCA EKRANU STARTOWEGO ------------------------

piwo = False

def pokaz_ekran_startowy() -> None:
    """"Zadaniem tej funkcji jest stworzenie okna początkowego, które zawiera"""
    # Stworzenie okna. Ten obiekt jest ważny, ponieważ jest on klasy Surface, czyli powierzchni, na którą można dodawać figury.
    intro_screen: pg.Surface = pg.display.set_mode(window_size)
    pg.display.set_caption("Koszmata 3.0")   # Tytuł okna


    """"""
    running: bool = True
    tytul_text: pg.Surface = font.render("Koszmata 3.0", True, WHITE)


    autorzy_text1:pg.Surface = mini_font.render("Autorzy: Natalia Jendrek, Natalia Koczkodaj, ",True, WHITE)
    autorzy_text2:pg.Surface = mini_font.render("Dominik Kowalczyk, Paweł Nowak, Szymon Smoła.",True, WHITE)


    zrodlo_zdjec1: pg.Surface = mini_font.render("Wszystkie zdjęcia zostały wygenerowane przez ",True, WHITE)
    zrodlo_zdjec2: pg.Surface = mini_font.render("Copilota za pomocą modelu DALL-E 2",True, WHITE)



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

        intro_screen.fill(LIGHT_BLUE) #Wypełnij okno startowe na pomarańczowo
        intro_screen.blit(tytul_text, (screen_width // 2 - tytul_text.get_width() // 2, 150)) #Dodaj tytuł gry na powierzchnie.
        intro_screen.blit(autorzy_text1, (50, 250)) #Dodaj autorów na powierzchnie.
        intro_screen.blit(autorzy_text2, (25, 270)) #Dodaj autorów  na powierzchnie.

        intro_screen.blit(zrodlo_zdjec1, (50, window_size[1]-50)) #Dodaj informacje o źródle zdjęć.
        intro_screen.blit(zrodlo_zdjec2, (65, window_size[1]-30)) #Dodaj informacje o źródle zdjęć.




        intro_screen.blit(graj_text, graj_rect) #Dodaj przycisk graj na powierzchnie

        intro_screen.blit(polecenie_text, polecenie_rect) #Dodaj okno z zachętą do rozpoczęcia gry.
        for instrukcja_text, instrukcja_rect in zip(instrukcja_texts, instrukcja_rects):
            intro_screen.blit(instrukcja_text, instrukcja_rect)

        pg.display.update()

pokaz_ekran_startowy()


def draw_text(text:str, 
              font:pg.font.Font, color:tuple[int], 
              surface:pg.Surface, 
              x:float, y:float) ->None:
    
    """Ta funkcja rysuje tekst o treści 'text', którego czcionka jest określona przez argument font, a kolor jest określony
    przez parametr color. 
    Umiejscowienie tekstu jest zależne od pary (x,y). 
    Argument surface jest okienkiem, na którym chcemy wyrenderować tekst."""
    
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def ObliczCzasTrwaniaGry(czastrwaniagry:float) -> tuple[int, int]:
    """Funkcja oblicza ile minęło pełnych minut oraz pełnych sekund od momentu rozpoczęcia rozgrywki."""
    game_time_minutes:int = int(czastrwaniagry // 60)
    game_time_seconds:int = int(czastrwaniagry % 60)


    return game_time_minutes, game_time_seconds


#Ekran wyświetlany pod koniec gry.
def game_over_screen() -> bool:
    """"Funkcja ta zajmuje się wyświetlaniem ekranu końcowego, na którym wyświetlane są podstawowe
    statystyki, takie jak: nasza dokładność, liczba zdobytych przez nas punktów oraz czas gry. 
    Zwraca wartość bool równa True, jeżeli użytkownik chce zagrać ponownie, lub wartość False, gdy użytkownik ma dość gry."""
    global game_time, shots_attempted, shots_scored
    

    #pg.time.get_ticks() zwraca wynik w milisekundach, więc zamień tę wartość na sekundy, dzieląc przez 1000.
    game_time = (pg.time.get_ticks() - czas_startu_gry)/1000
    
    game_time_minutes, game_time_seconds = ObliczCzasTrwaniaGry(game_time)  #Oblicz ile pełnych minut oraz ile pełnych sekund minęło 
                                                                                  #Od startu gry do końca gry.

    end_button_rect = pg.Rect((window_size[0] - end_button_width) // 2, window_size[1] - 100, end_button_width, end_button_height)

    #Policz dokładnośc naszych strzałów, zaokrąglij ją.
    accuracy:float =  round((shots_scored / shots_attempted) * 100,2)


    
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

                    ending_theme.stop()

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


    screen.fill(color = WHITE, )


    tablica = Klasy.Tablica(anchor = [screen_width//2 - tablica_szerokość//2,screen_height*1//5-tablica_wysokość//2],
                            color = tablica_kolor, width = tablica_szerokość, height = tablica_wysokość) #Definicja obiektu typu Tablica
    tablica.NarysujProstokąt(screen = screen) #Rysowanie tablicy


    kosz = Klasy.Obrecz(anchor = [screen_width//2 - kosz_szerokość//2,screen_height*1//5+tablica_wysokość//2-kosz_wysokość],
                        color = kosz_kolor, width = kosz_szerokość, height = kosz_wysokość) #Definicja obiektu typu Obrecz.
  

    kosz.NarysujProstokąt(screen = screen) #Rysowanie obręczy (inaczej nazywany koszem)

    return screen, tablica, kosz

def ZnajdźTła() -> tuple[list[pg.Surface], int]:
    """Funkcja zajmuje się znalezieniem listy wszystkich tieł, 
    które będą zmieniały się w grze
    """
    Folder_Z_Tłami = path.Path(r"TłaDoGry")

    ListaTeł:int = len([plik for plik in Folder_Z_Tłami.iterdir() if plik.is_file()]) 

    NazwyTeł =[Folder_Z_Tłami/f"TłoGry{i+1}.jpg" for i in range(0,ListaTeł)]


    return [pg.image.load(Tło) for Tło in NazwyTeł], max_shots//len(NazwyTeł)



#game_screen jest okienkiem, na którym rysujemy obiekty będącę interaktywnymi elementami rozgrywki.
#tablica reprezentuje cały obiekt, na którym zawiszony jest kosz.
#kosz jest z kolei celem, w którego trafienie jest najważniejszym zadaniem gry.
game_screen, tablica, kosz  = NarysujEkranRozgrywki()


Działo:Klasy.Cannon =Klasy.Cannon(x0 = window_size[0]/2, y0=window_size[1]-125, #Po naciśnieciu przycisku start stwórz armatę
                                  width = 50,  height = 100,) #która domyślnie jest wypionizowana (tj. jej nachylenie wynosi 90 stopni)

Działo.NarysujArmatę(screen = game_screen, color = BLACK) #Teraz narysuj tę armatę.




#Poniższe cztery zmienne będą wykorzystywane do statystyk.
shots_attempted:int = 0  #Liczba oddanych strzałów (celnych lub niecelnych)
shots_scored:int = 0 #Celne strzały.
game_time:float = 0 #Czas trwania gry (od momentu nacisnięcia przycisku "GRAJ")
max_shots:int = 12 #Maksymalna liczba dozwolonych strzałów. Po przekroczeniu jej, ekran rozgrywki przechodzi do ekranu końcowego.
#Uwaga, liczba zdjęc musi być dzielnikiem liczby max_shots.

#Zmienna mówiąca, czy kula zostala wystrzelona.
shot_ball: bool = False


#Moment rozpoczęcia gry. Będzie ta zmienna ważna przy podsumowaniu statystyk.
czas_startu_gry = pg.time.get_ticks()

#Zmienna, która odpowiada za trwanie rozgrywki.
running:bool = True


ZdjęciaTeł, OdstępPunktowy = ZnajdźTła()

PasekDolnyLewy = Klasy.Prostokąt(anchor = [10, 690], color = BLACK, width =150 , height = 50)
PasekDolnyPrawy = Klasy.Prostokąt(anchor = [window_size[0] - 150-10, 690], color = BLACK, width =150 , height = 50)




while running:
        
        game_screen.blit(source = ZdjęciaTeł[shots_scored//OdstępPunktowy], #Aktualizuj tło.
                         dest = (screen_width//2 - 512,screen_height//2 - 512)) 
   
    
        #Tworzenie nowego działa.
        Działo = Klasy.Cannon(window_size[0]/2, window_size[1]-125, 50, 100)

        #Policz kąt nachylenia armaty.
        kąt =  Klasy.Cannon.PoliczKąt(Działo.x0, Działo.y0)
        
        #Jeżęli kąt nie jest równy False (czyli kąt nie jest równy 0 i nie jest równy pi), to zmień wartość kąta
        #Jeżęli kąt jest równy False, to kąt domyślnie jest równy pi/2, czyli armata jest wypionizowana.
        if kąt is not False:
            Działo.slope = kąt

        Działo.NarysujArmatę(screen = game_screen, color = BLACK)

                
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
                        #Odtwórz dźwięk eksplozji.
                        explosion_sound.play()
                        
                        Kula = Działo.WystrzelKulę(screen = game_screen, speed = 0.5)

                        #Ta zmienna shot_ball ustawi się ponownie na False, gdy kula (dotknię Tablicy lub obręczy) 
                        #lub gdy górny punkt piłki bedzie zbyt wysoko.
                        shot_ball = True

                        shots_attempted += 1

            
       
        if shot_ball is True:
    
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
                scoring_theme.play()

                shots_scored += 1
                shot_ball = False

                Kula.NarysujKule(screen = game_screen, 
                                 color = ORANGE) #Skasuj kulkę, gdy dotknie ona obręczy
                
            elif Obszar_Tablica.collidepoint(Kula.x, Kula.y):
        
                shot_ball = False 
                
                Kula.NarysujKule(screen = game_screen, 
                                 color = ORANGE) #Skasuj kulkę, gdy dotknie ona tablicy.
                

        #Czas gry
        game_time = (pg.time.get_ticks() - czas_startu_gry)/1000
        minutes, seconds = ObliczCzasTrwaniaGry(game_time)
    
        #Napraw kosz i tablicę.
        tablica.NarysujProstokąt(screen = game_screen)
        kosz.NarysujProstokąt(screen = game_screen)

        PasekDolnyLewy.NarysujProstokąt(screen = game_screen) #Lewy dolny prostokąt, liczący liczbę punktów zdobytych na liczbę oddanych strzałów
        PasekDolnyPrawy.NarysujProstokąt(screen = game_screen) #Prawy dolny prostokąt, liczący czas trwania gry.


        draw_text(text = f"{minutes}:{seconds}", font= small_font, color = LIGHT_BLUE, surface = game_screen,
                  x = PasekDolnyPrawy.anchor[0] + 75, y = PasekDolnyPrawy.anchor[1]+25) #Dodaj etykiete na PasekLewyDolny.
        
        draw_text(text = f"{shots_scored}/{shots_attempted}", font= small_font, color = LIGHT_BLUE, surface = game_screen,
                  x = PasekDolnyLewy.anchor[0] + 75, y = PasekDolnyLewy.anchor[1]+25) #Dodaj etykietę na PrawyDolnyPrawy.
        



        
        if shots_attempted >= max_shots and shot_ball == False:
            #Odtwórz jingiel końcowy.
            ending_theme.play()
            # Wyświetl ekran końcowy
            czy_kontynuować = game_over_screen()


            #Jeżeli gracz chce kontynuować grę, zresetuj grę.
            if czy_kontynuować == True:
                screen, tablica, kosz = NarysujEkranRozgrywki()

                czas_startu_gry = pg.time.get_ticks()

                shot_ball = False
            else:
                break
        
        
        ### Schemat odbijania się kosza.
        if tablica.center[0] <= tablica.width/2 or window_size[0] - tablica.center[0]<=tablica.width/2:
            tablica.speed = -tablica.speed
     
        tablica.ZmieńWspółrzędne() #Aktualizuj współrzędne.
        tablica.ZmieńSzybkość(shots_scored = shots_scored, max_shots = max_shots) #Zaaktualizuj szybkość tablicy.
        




        #Narysuj nową obręcz
        kosz = Klasy.Obrecz(anchor = [ tablica.width/2 - kosz.width/2 + tablica.anchor[0],   screen_height*1//5+tablica_wysokość//2-kosz_wysokość], 
                           color = ORANGE, width = kosz.width, 
                    height =  kosz.height, ile_zmniejszeń = kosz.ile_zmniejszeń) 
        
        #Zmniejsz obręcz
        kosz.PomniejszObręcz(shots_scored = shots_scored,
                             max_shots = max_shots)
        
            
        pg.display.update() #Zaaktualizuj ekran.
