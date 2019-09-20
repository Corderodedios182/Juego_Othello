
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 21:05:13 2019

@author: carlos
"""

# Reversi

import random
import sys

def dibujarTablero(tablero):
    
    # Esta funcion dibuja el tablero recibido. Devuelve None.
    LÍNEAH = '  +---+---+---+---+---+---+---+---+'
    LÍNEAV = '  |   |   |   |   |   |   |   |   |'
    
    print('    1   2   3   4   5   6   7   8')
    print(LÍNEAH)

    for y in range(8):
        print(LÍNEAV)
        print(y+1, end=' ')
        
        for x in range(8):
            print('| %s' % (reiniciarTablero[x][y]), end=' ')
            print('|')
            print(LÍNEAV)
            print(LÍNEAH)
 
           
def reiniciarTablero(tablero):
    # Deja en blanco el tablero recibido como argumento, excepto la posición inicial.
    for x in range(8):
        for y in range(8):
            tablero[x][y] = ' '
            # Piezas iniciales:
    
    tablero[3][3] = 'X'
    tablero[3][4] = 'O'
    tablero[4][3] = 'O'
    tablero[4][4] = 'X'
    

def obtenerNuevoTablero():
    # Crea un tablero nuevo, vacío.
    tablero= []
    for i in range(8):
        tablero.append([' '] * 8)
    
    return tablero
    
    








