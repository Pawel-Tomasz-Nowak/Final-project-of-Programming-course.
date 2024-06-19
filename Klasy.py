import pygame as pg
import numpy as np
from Stałe import screen_width, screen_height, window_size
from Stałe import ORANGE, WHITE, MEDIUM_GRAY, BLACK, LIGHT_BLUE
from Stałe import font, small_font, mini_font
from Stałe import end_button_width, end_button_height, end_button_color, end_button_text_color
from Stałe import tablica_kolor, tablica_szerokość, tablica_wysokość
from Stałe import kosz_kolor, kosz_szerokość, kosz_wysokość, k



class Prostokąt():
    def __init__(self, anchor:list[float], color:list[int], width:float, height:float):
        self.anchor = anchor #TO
        self.color = color #TO

        self.width = width #TO
        self.height = height #TO

        self.center = (self.anchor[0] + width/2, self.anchor[1]-height/2) #TO

        #Szybkość poruszania się tablicy w poziomie.
        self.speed = 0 #T
        

    
    def NarysujProstokąt(self,screen:pg.Surface):
        """Metoda ta rysuje prostokąt na ekranie screen."""    
        tablica = pg.Rect(self.anchor[0], self.anchor[1], self.width, self.height)
        
        pg.draw.rect(surface = screen, 
                     color = self.color, 
                     rect = tablica)
        

class Tablica(Prostokąt):
    def __init__(self, anchor:list[float], color:list[int], width:float, height:float, speed:float = 0,ile_zmian_szybkosci:int = 0):
        super().__init__(anchor = anchor, color = color, width = width, height = height)
        self.ile_zmian_szybkosci = ile_zmian_szybkosci
        self.speed = speed

       #To jest metoda dla tablicy.


    def ZmieńSzybkość(self, shots_scored:int, max_shots:int):
        for i in range(1, 5):
            if shots_scored >= max_shots//4*(i) and self.ile_zmian_szybkosci == i-1:
                if i == 1:
                    self.speed = 0.1
                else:
                    self.speed = self.speed * 2
                
                self.ile_zmian_szybkosci += 1

    def ZmieńWspółrzędne(self):
        """Metoda ta aktualizuje pierwsza współrzędna punktu kotwiczego o wartość speed. 
        Przez pierwszą fazę gdy speed = 0, zatem wartość
        pierwszej współrzędnej się nie zmienia
        """
        
        self.anchor[0] = self.anchor[0] + self.speed #Zmień x-ową współrzędna.

        self.center = (self.anchor[0] + self.width/2, self.anchor[1]-self.height/2) #Zaaktualizuj środek tablicy.

 


class Obrecz(Prostokąt):

    def __init__(self, anchor:list[float], color:list[int], width:float, height:float, ile_zmniejszeń:int =0):
        """Inicjalizacja obiektu klasy Obrecz"""
        super().__init__(anchor = anchor, color = color, width = width, height = height)

        self.ile_zmniejszeń = ile_zmniejszeń

       #To jest metoda dla obręczy.
    def PomniejszObręcz(self, shots_scored:int, max_shots:int) -> None:
        """Metoda ta pomniejsza szerokość obręczy w zależności od liczby trafionych strzałów.
        Co max_shots//4 trafionych strzałów szerokość obręczy zmniejsza się o (1-k) procent
        """

        for i in range(1,5):
             if shots_scored >= max_shots//4*(i) and self.ile_zmniejszeń == i-1:
                self.width = self.width * k
                self.ile_zmniejszeń += 1



        

class Point():
    def __init__(self, x:float, y:float) ->None:
        self.x:float = x #Współrzędna x-owa punktu.
        self.y:float = y #Współrzędna y-owa punktu.




class CannonBall():
    def __init__(self, x:float, y:float, r:float, speed:float, alpha:float) -> None:
        #Współrzędne środka kuli.
        self.x = x
        self.y = y

        #Promień kuli
        self.r = r

        #Wyznacz wspólrzędne wektora prędkości.
        self.dx = np.cos(alpha)*speed
        self.dy = np.sin(alpha)*speed

        #Licz ile razy piłka się odbiła
        self.n_odbic = 0
        



    def NarysujKule(self, screen: pg.Surface, color: list[int] = (100, 100, 100)) -> None:
        pg.draw.circle(surface = screen, color = color, 
                       center = (self.x, self.y), radius = self.r)
        


    def AktualizujWspółrzędne(self) -> None:
        self.x = self.x + self.dx
        self.y = self.y - self.dy
        

class Cannon():


    def __init__(self, x0:float, y0:float, width:float, height:float, slope:float = np.pi/2) -> None:
        self.x0 = x0
        self.y0 = y0


        self.width = width
        self.height = height
        self.slope = slope

        self.wierzch: list[Point] = []



    def ZnajdźWierzchołki(self, kąt: float = 0) -> None:
        #Policz pierwszy wierzchołek.
        x1 = self.x0 - np.sin(kąt)*self.width/2
        y1 = self.y0 - np.cos(kąt)*self.width/2

        #Teraz drugi.
        x2 = self.x0 + np.sin(kąt)*self.width/2
        y2 = self.y0 + np.cos(kąt)*self.width/2

        #A teraz trzeci.
        x3 = x1+ np.cos(kąt)*self.height
        y3 = y1 - np.sin(kąt)*self.height

        #I czwarty.
        x4 = x2 + np.cos(kąt)*self.height
        y4 = y2 - np.sin(kąt)*self.height

        #Zaaktualizuj listę wierzchołków.
        P1 = Point(x1,y1)
        P2 = Point(x2,y2)
        P3 = Point(x3,y3)
        P4 = Point(x4,y4)

        self.wierzch = [P1, P2, P4, P3]

        self.wierzch_cords = [(Punkt.x, Punkt.y) for Punkt in self.wierzch]
    



    @staticmethod
    #Domyślnie x2 y2 to współrzędne myszki.
    #W skrajnym przypadku, gdy współrzedna y-oka myszki jest mniejsza niż współrzędna y-owa środka armaty, zwróć wartość logiczną False.
    def PoliczKąt(x1:float, y1:float) -> float | int:
        x2, y2 = pg.mouse.get_pos()

        if y2 < y1:
            if x1 != x2:
                tangens = (y2 - y1)/(x1-x2)

                return np.arctan(tangens) + (np.pi if tangens <0 else 0)


            else:
                return np.pi/2
            
        else:
            if x2 > x1:
                return 0
            elif x2 < x1:
                return np.pi
            else:
                return np.pi/2
            
            
    def NarysujArmatę(self, screen: pg.Surface, color:tuple[int] =(0,0,0)) ->None:
        self.ZnajdźWierzchołki(self.slope)

            
        pg.draw.polygon(surface = screen, 
                            color  = color, 
                            points = self.wierzch_cords)
            

        pg.draw.circle(surface = screen, 
            color = color, center = (self.x0, self.y0), radius = self.width/2)
        

    
    def WystrzelKulę(self, screen:pg.Surface, speed:float) -> CannonBall:
        assert speed >0, "Szybkość musi być dodatnią liczbą"
        
        #Promień kuli.
        r = 15

        #Policz współrzędne środka kuli.
        ball_x = self.x0 + np.cos(self.slope)*(self.height+2*r)
        ball_y = self.y0 - np.sin(self.slope)*(self.height+2*r)

        Kula = CannonBall(ball_x, ball_y, r, speed = speed, alpha = self.slope)
        Kula.NarysujKule(screen)

        return Kula


            







