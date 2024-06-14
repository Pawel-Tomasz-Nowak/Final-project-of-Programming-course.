import pygame as pg
import numpy as np
#from Stałe import screen_width, screen_height




class Prostokąt():
    def __init__(self, anchor:list[float], color:list[int], width:float, height:float):
        self.anchor = anchor
        self.color = color

        self.width = width
        self.height = height

        self.center = (self.anchor[0] + width/2, self.anchor[1]-height/2)

        #Szybkość poruszania się tablicy w poziomie.
        self.speed = 0

        




    def NarysujProstokąt(self,screen):    
        tablica = pg.Rect(self.anchor[0], self.anchor[1], self.width, self.height)
        
        pg.draw.rect(surface = screen, 
                     color = self.color, 
                     rect = tablica)
        
    def ZmieńWspółrzędne(self):
        self.anchor[0] = self.anchor[0] + self.speed

        self.center = (self.anchor[0] + self.width/2, self.anchor[1]-self.height/2)



        


class Point():
    def __init__(self, x:float, y:float) ->None:
        self.x:float = x
        self.y:float = y




class CannonBall():
    def __init__(self, x:float, y:float, r:float, speed:float, alpha:float):
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
        



    def NarysujKule(self, screen: pg.Surface, color: list[int] = (100, 100, 100)):
        pg.draw.circle(surface = screen, color = color, 
                       center = (self.x, self.y), radius = self.r)
        


    def AktualizujWspółrzędne(self):
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



    def ZnajdźWierzchołki(self, kąt: float = 0):
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
    def PoliczKąt(x1:float, y1:float) -> float | bool:
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


            







