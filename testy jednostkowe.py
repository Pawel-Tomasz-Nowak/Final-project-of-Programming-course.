import pytest
import numpy as np
import pygame as pg
from Klasy import Prostokąt, Tablica, Obrecz, Point, CannonBall, Cannon 

# Inicjalizacja Pygame
pg.init()
screen = pg.display.set_mode((800, 600))

def test_prostokat_init():
    prostokat = Prostokąt(anchor=[100, 200], color=[255, 0, 0], width=50, height=100)
    assert prostokat.anchor == [100, 200]
    assert prostokat.color == [255, 0, 0]
    assert prostokat.width == 50
    assert prostokat.height == 100
    assert prostokat.center == (125, 150)

def test_tablica_init():
    tablica = Tablica(anchor=[100, 200], color=[255, 0, 0], width=50, height=100, speed=1.0, ile_zmian_szybkosci=2)
    assert tablica.anchor == [100, 200]
    assert tablica.color == [255, 0, 0]
    assert tablica.width == 50
    assert tablica.height == 100
    assert tablica.speed == 1.0
    assert tablica.ile_zmian_szybkosci == 2

def test_tablica_zmiana_szybkosci():
    tablica = Tablica(anchor=[100, 200], color=[255, 0, 0], width=50, height=100, speed=0, ile_zmian_szybkosci=0)
    tablica.ZmieńSzybkość(shots_scored=10, max_shots=40)
    assert tablica.speed == 0.1
    assert tablica.ile_zmian_szybkosci == 1

def test_cannonball_init():
    ball = CannonBall(x=100, y=200, r=15, speed=5.0, alpha=np.pi/4)
    assert ball.x == 100
    assert ball.y == 200
    assert ball.r == 15
    assert ball.dx == pytest.approx(5.0 * np.cos(np.pi/4))
    assert ball.dy == pytest.approx(5.0 * np.sin(np.pi/4))

def test_cannon_init():
    cannon = Cannon(x0=400, y0=300, width=50, height=100, slope=np.pi/2)
    assert cannon.x0 == 400
    assert cannon.y0 == 300
    assert cannon.width == 50
    assert cannon.height == 100
    assert cannon.slope == np.pi/2

def test_cannonball_aktualizuj_wspolrzedne():
    ball = CannonBall(x=100, y=200, r=15, speed=5.0, alpha=np.pi/4)
    ball.AktualizujWspółrzędne()
    assert ball.x == pytest.approx(100 + 5.0 * np.cos(np.pi/4))
    assert ball.y == pytest.approx(200 - 5.0 * np.sin(np.pi/4))


