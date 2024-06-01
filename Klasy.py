import pygame as pg
import numpy as np
import sys

class Point():



    def __init__(self, x:float, y:float) ->None:
        self.x = x
        self.y = y




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
            return False
        
            
    def NarysujArmatę(self, surface: pg.Surface, color:tuple[int] =[0,0,0]) ->None:
        self.ZnajdźWierzchołki(self.slope)

            
        pg.draw.polygon(surface = surface, 
                            color  = color, 
                            points = self.wierzch_cords)
            

        pg.draw.circle(surface = surface, 
            color = color, center = (self.x0, self.y0), radius = self.width/2)
            







