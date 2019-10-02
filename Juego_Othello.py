# Reversi		

#En las primeras lineas del codigo defino las funciones que posterirmente ocupo para jugar.

#Importando Modulos
import random
import sys		

#########################################################
#La estructura del Tablero de Datos del Tablero de Juego#
#########################################################

#La estructura es una lista de listas. La lista de listas se crea para que tablero[x][y] represente al caracter en la posicion 
#x sobre el eje X (izquierda a derecha) y la posicion y sobre el eje Y (arriba hacia abajo).

#La funcion dibujarTablero() imprime el tablero actual del juego basado en la estrucutra de datos en la variable tablero.
def dibujarTablero(tablero):		
    # Esta funcion dibuja el tablero recibido. Devuelve None		
    LÍNEAH = '  +---+---+---+---+---+---+---+---+'		
    LÍNEAV = '  |   |   |   |   |   |   |   |   |'		
		
    print('    1   2   3   4   5   6   7   8')		
    print(LÍNEAH)		
    for y in range(8):		
        print(LÍNEAV)		
        print(y+1, end=' ')		
        for x in range(8):		
            print('| %s' % (tablero[x][y]), end=' ')		
        print('|')		
        print(LÍNEAV)		
        print(LÍNEAH)		
		
#Permite comenzar un nuevo juego
def reiniciarTablero(tablero):		
    # Deja en blanco el tablero recibido como argumento, excepto la posición inicial		
    for x in range(8):		
        for y in range(8):		
            tablero[x][y] = ' '		
		
    # Piezas iniciales:		
    tablero[3][3] = 'X'		
    tablero[3][4] = 'O'		
    tablero[4][3] = 'O'		
    tablero[4][4] = 'X'		
		
#Crea una nueva estructura de datos tablero y la devuelve, crea las 8 listas internas. Los espacios representan un tablero de juego completamente vacio
#Lo que la variable tablero termina siendo es una lista de 8 listas, y cada una de esas listas tiene 8 cadenas. El resultado son 64 cadenas '' con un caracter espacio.
def obtenerNuevoTablero():		
    # Crea un tablero nuevo, vacío.		
    tablero = []		
    for i in range(8):		
        tablero.append([' '] * 8)		
		
    return tablero		

#############################################################################################################################################################
#Comprobando si una Jugada es Válida
#Dada una estructura de datos tablero, la baldosa del jugador y la coordenadas XY de la jgada del jugador, esJugadaVálida() devuelve True si las reglas de
#Othello permiten una jugada en esas coordenadas y False en caso contrario.
#
#1) Pertenecer al tablero
#   
#2) Convertir (tocar) almenos una pieza del otro jugador
#############################################################################################################################################################
def esJugadaVálida(tablero, baldosa, comienzox, comienzoy):
    # Devuelve False si la jugada del jugador en comienzox, comienzoy es invalida		
    # Si es una jugada válida, devuelve una lista de espacios que pasarían a ser del jugador si moviera aquí.
    #Comprueba si las coordenadas XY estan fuera del tablero, o si el espacio no esta vacio. estanEnTablero() es una funcion definida mas adelante en el programa 
    #que se asegura de que el valor de ambas coordenadas X e Y este comprendido entre 0 y 7.
    if tablero[comienzox][comienzoy] != ' ' or not estáEnTablero(comienzox, comienzoy): #Validamos que la jugada se encuentra dentro del tablero
        return False		
		
    tablero[comienzox][comienzoy] = baldosa # coloca temporariamente la baldosa sobre el tablero.		
		
    if baldosa == 'X':
        otraBaldosa = 'O'
    else:
        otraBaldosa = 'X'
		
    baldosasAConvertir = []
    
    #El bucle for nos indica las direcciones que puede moverse una jugada dada    
    for direcciónx, direccióny in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:		
        #Se modifican las variables x e y para moverse en las dirreciones determinadas por direccionx y direcciony.
        x, y = comienzox, comienzoy
        x += direcciónx # primer paso en la dirección		
        y += direccióny # primer paso en la dirección		
        
        #Para que sea una jugada valida:
        
        #1)Pertenecer al tablero
        if estáEnTablero(x, y) and tablero[x][y] == otraBaldosa:		
            # Hay una pieza perteneciente al otro jugador al lado de nustra pieza		
            x += direcciónx		
            y += direccióny		
            if not estáEnTablero(x, y):		
                continue
            
            #2) Convertir piezas del otro jugador
            while tablero[x][y] == otraBaldosa:		
                x += direcciónx		
                y += direccióny		
                if not estáEnTablero(x, y): # sale del bucle while y continua en el bucle for.		
                    break		
            if not estáEnTablero(x, y):		
                continue		
            if tablero[x][y] == baldosa:		
                # Hay fichas a convertir. Caminar en dirección opuesta hasta llegar al casillero original, registrando todas las posiciones en el camino.		
                while True:		
                    x -= direcciónx		
                    y -= direccióny		
                    if x == comienzox and y == comienzoy:		
                        break		
                    baldosasAConvertir.append([x, y])		
		
    tablero[comienzox][comienzoy] = ' ' # restablecer el espacio vacío		
    if len(baldosasAConvertir) == 0: # Si no se convirtió ninguna baldosa, la jugada no es válida.		
        return False		
    return baldosasAConvertir		


def estáEnTablero(x, y):		
    # Devuelve True si las coordenadas se encuentran dentro del tablero		
    return x >= 0 and x <= 7 and y >= 0 and y <=7		

####################################################################################################################################################
#OBTENIENDO UNA LISTA CON TODAS LAS JUGADAS VALIDAS
#
#Aqui se comienza la creacion del Arbol de Juego con las posibles jugadas que se pueden realizar en el siguiente estado
#
#La funcion obtenerJugadasValidas(), devuelves una lista de listas de dos elementos. Estas listas contienen las coordenadas XY de todas las jugadas
#validas para el jugador correspondiente (sea jugador o computadora).
#Esta funcion usa bucles anidados para comprobar cada par de coordenadas XY (las 64 combinaciones posibles) llamando a esJugadaValida() en cada iteracion.
#Con esto se representa el Arbol de Juego, visualizando las jugadas con la funcion obtenerTableroConJugadasValidas()
########################################################################################################################################################
    
def obtenerJugadasVálidas(tablero, baldosa):
    # Devuelve una lista de listas [x,y] de jugadas válidas para el jugador en el tablero dado.		
    jugadasVálidas = []		
		
    for x in range(8):		
        for y in range(8):		
            if esJugadaVálida(tablero, baldosa, x, y) != False:		
                jugadasVálidas.append([x, y])		
    return jugadasVálidas		
		
#Representacion del Arbol de Juegadas, mas adelante especificamos la mejor jugada para la maquina.
def obtenerTableroConJugadasVálidas(tablero, baldosa):		
    # Devuelve un nuevo tablero, marcando con "." las jugadas válidas que el jugador puede realizar.		
    réplicaTablero = obtenerCopiaTablero(tablero)		
		
    for x, y in obtenerJugadasVálidas(réplicaTablero, baldosa):		
        réplicaTablero[x][y] = '.'		
    return réplicaTablero		
		

#########################################################################################
#FUNCIONES DE INTERACCION 
#Obteniendo el Puntaje del Tablero de Juego
#Obteniendo la Opcion de Baldosa del Jugador
#Determinado Quién Comienza
#Preguntar al Jugador si Quiere Jugar de Nuevo
#Mostrar Puntajes actuales del juego
########################################################################################
    
def obtenerPuntajeTablero(tablero):		
    # Determina el puntaje contando las piezas. Devuelve un diccionario con claves 'X' y 'O'.		
    puntajex = 0		
    puntajeo = 0		
    for x in range(8):		
        for y in range(8):		
            if tablero[x][y] == 'X':		
                puntajex += 1		
            if tablero[x][y] == 'O':		
                puntajeo += 1		
    return {'X':puntajex, 'O':puntajeo}		
		
		
def ingresarBaldosaJugador():
    # Permite al jugador elegir que baldosa desea ser.		
    # Devuelve una lista con la baldosa del jugador como primer elemento y el de la computadora como segundo.		
    baldosa = ''		
    while not (baldosa == 'X' or baldosa == 'O'):		
        print('¿Deseas ser X ó O?')		
        baldosa = input().upper()		
		
    #  El primer elemento en la lista es la baldosa del juegador, el segundo es la de la computadora.		
    if baldosa == 'X':		
        return ['X', 'O']		
    else:		
        return ['O', 'X']		
		
		
def quiénComienza():		
    # Elije al azar qué jugador comienza.		
    if random.randint(0, 1) == 0:		
        return 'computadora'		
    else:		
        return 'jugador'		
		
def jugarDeNuevo():		
    # Esta función devuelve True si el jugador quiere jugar de nuevo, de lo contrario devuelve False.		
    print('¿Quieres jugar de nuevo? (sí o no)')		
    return input().lower().startswith('s')		


def mostrarPuntajes(baldosaJugador, baldosaComputadora):		
    # Imprime el puntaje actual.		
    puntajes = obtenerPuntajeTablero(tableroPrincipal)		
    print('Tienes %s puntos. La computadora tiene %s puntos.' % (puntajes[baldosaJugador], puntajes[baldosaComputadora]))		
		
#########################################################################################################################################
#Funciones para el DESAROOLLO DEL JUEGO
#hacerJugada (colocar una baldosa en el tablero y convertir otras fichas de acuerdo con las reglas del reversi)
#obtenerCopiaTablero (hace una copia para hacer pruebas sin afectar el tablero final)
#esEsquina  
#obtenerJugadaJugador (Almacenar la jugada del jugador)
#########################################################################################################################################
    
def hacerJugada(tablero, baldosa, comienzox, comienzoy):		
    # Coloca la baldosa sobre el tablero en comienzox, comienzoy, y convierte cualquier baldosa del oponente.		
    # Devuelve False si la jugada es inválida, True si es válida.		
    baldosasAConvertir = esJugadaVálida(tablero, baldosa, comienzox, comienzoy)		
		
    if baldosasAConvertir == False:		
        return False		
		
    tablero[comienzox][comienzoy] = baldosa		
    for x, y in baldosasAConvertir:		
        tablero[x][y] = baldosa		
    return True		
		
		
def obtenerCopiaTablero(tablero):		
    # Duplica la lista del tablero y devuelve el duplicado.		
    réplicaTablero = obtenerNuevoTablero()		
		
    for x in range(8):		
        for y in range(8):		
            réplicaTablero[x][y] = tablero[x][y]		
		
    return réplicaTablero		
		
		
def esEsquina(x, y):		
    # Devuelve True si la posicion es una de las esquinas.		
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)		
		
		
def obtenerJugadaJugador(tablero, baldosaJugador):		
    # Permite al jugador tipear su jugada.		
    # Devuelve la jugada como [x, y] (o devuelve las cadenas 'pistas' o 'salir')		
    CIFRAS1A8 = '1 2 3 4 5 6 7 8'.split()		
    while True:		
        print('Ingresa tu jugada en este orden xy ejemplo 46, si deseas terminar el juego solo ingresa la palabra salir, o la paralabra pistas para activar/desactivar las pistas.')		
        jugada = input().lower()		
        if jugada == 'salir':		
            return 'salir'		
        if jugada == 'pistas':		
            return 'pistas'		
		
        if len(jugada) == 2 and jugada[0] in CIFRAS1A8 and jugada[1] in CIFRAS1A8:		
            x = int(jugada[0]) - 1		
            y = int(jugada[1]) - 1		
            if esJugadaVálida(tablero, baldosaJugador, x, y) == False:		
                continue		
            else:		
                break		
        else:		
            print('Esta no es una jugada válida. Ingresa la coordenada x (1-8), luego la coordenada y (1-8).')		
            print('Por ejemplo, 81 corresponde a la esquina superior derecha.')		
		
    return [x, y]		
		
########################################################################################################
#Heuristica con busqueda informada
#La maquina analiza los posibles estados siguientes y en base a ese conocimiento toma la mejor opcion
#1) Ejecuta las posibles jugadas
#2) Cuenta las fichas convertidas en cada jugada
#3) Se queda con la que genere un mayor numero de fichas a su favor
#########################################################################################################
def obtenerJugadaComputadora(tablero, baldosaComputadora):
    # Dado un tablero y la baldosa de la computadora, determinar dónde		
    # jugar y devolver esa jugada como una lista [x, y].		
    if dificultad == 'Novato':
        #Solo toma la primera jugada que le aparesca en jugadasPosibles
        jugadasPosibles = obtenerJugadasVálidas(tablero, baldosaComputadora)
		# ordena al azar el orden de las jugadas posibles		
        random.shuffle(jugadasPosibles)
        
        for x, y in jugadasPosibles:
           if esEsquina(x, y):
               return [x, y]
           
        return jugadasPosibles[0]
        
    elif dificultad == 'Intermedio':
        #Juega la jugada que conviera mayor numero de piezas
       jugadasPosibles = obtenerJugadasVálidas(tablero, baldosaComputadora)
       # ordena al azar el orden de las jugadas posibles		
       random.shuffle(jugadasPosibles)
       # siempre jugar en una esquina si está disponible.		
       for x, y in jugadasPosibles:
           if esEsquina(x, y):
               return [x, y]
		
        # Recorrer la lista de jugadas posibles y recordar la que da el mejor puntaje
        ###################################################################
        #Algoritmo IA para jugar contra la maquina
        #Analizando las jugadas y se queda con la que mejor puntaje
        ###################################################################
       mejorPuntaje = -1
       for x, y in jugadasPosibles:
           réplicaTablero = obtenerCopiaTablero(tablero)
           hacerJugada(réplicaTablero, baldosaComputadora, x, y)
           puntaje = obtenerPuntajeTablero(réplicaTablero)[baldosaComputadora]
           if puntaje > mejorPuntaje:
            mejorJugada = [x, y]
            mejorPuntaje = puntaje
       return mejorJugada
		
    else:
        return "dificultad no valida"

#####################
#Ejecucion del juego#
#####################
		
print('¡Bienvenido a Reversi!')		
		
while True:		
    # Reiniciar el tablero y el juego.		
    tableroPrincipal = obtenerNuevoTablero()
    reiniciarTablero(tableroPrincipal)		
    baldosaJugador, baldosaComputadora = ingresarBaldosaJugador()
    mostrarPistas = False		
    turno = quiénComienza()		
    print(("El " if turno == "jugador" else "La ") + turno + ' comienza.')
    dificultad = input("Ingresa la dificultad, 1 = Novato, 2 = Intermedio, 3 = Experto) : ")
    if dificultad == str(1):
        dificultad = 'Novato'
    elif dificultad == str(2):
        dificultad = 'Intermedio'
    else:
        dificultad = 'Experto'

    while True:		
        if turno == 'jugador':
            # Turno del jugador		
            if mostrarPistas:
                tableroConJugadasVálidas = obtenerTableroConJugadasVálidas(tableroPrincipal, baldosaJugador)		
                dibujarTablero(tableroConJugadasVálidas)		
            else:		
                dibujarTablero(tableroPrincipal)		
            mostrarPuntajes(baldosaJugador, baldosaComputadora)		
            jugada = obtenerJugadaJugador(tableroPrincipal, baldosaJugador)		
            if jugada == 'salir':		
                print('¡Gracias por jugar!')		
                sys.exit() # terminar el programa		
            elif jugada == 'pistas':		
                mostrarPistas = not mostrarPistas		
                continue		
            else:		
                hacerJugada(tableroPrincipal, baldosaJugador, jugada[0], jugada[1])		
		
            if obtenerJugadasVálidas(tableroPrincipal, baldosaComputadora) == []:		
                break		
            else:		
                turno = 'computadora'		
		
        else:		
            # Turno de la computadora		
            dibujarTablero(tableroPrincipal)		
            mostrarPuntajes(baldosaJugador, baldosaComputadora)		
            input('Presiona enter para ver la jugada de la computadora.')		
            x, y = obtenerJugadaComputadora(tableroPrincipal, baldosaComputadora) #Llama a la funcion obtenerJugadaComputadora
            hacerJugada(tableroPrincipal, baldosaComputadora, x, y) #Realiza la mejor jugada para la computadora
		
            if obtenerJugadasVálidas(tableroPrincipal, baldosaJugador) == []:		
                break		
            else:		
                turno = 'jugador'		
		
    # Mostrar el puntaje final.		
    dibujarTablero(tableroPrincipal)		
    puntajes = obtenerPuntajeTablero(tableroPrincipal)		
    print('X ha obtenido %s puntos. O ha obtenido %s puntos.' % (puntajes['X'], puntajes['O']))
    if puntajes[baldosaJugador] > puntajes[baldosaComputadora]:		
        print('¡Has vencido a la computadora dificultad %s , por %s puntos! ¡Felicitaciones!' % (dificultad,puntajes[baldosaJugador] - puntajes[baldosaComputadora]))
    elif puntajes[baldosaJugador] < puntajes[baldosaComputadora]:		
        print('Has perdido. La computadora te ha vencido dificultad %s , por %s puntos.' % (dificultad, puntajes[baldosaComputadora] - puntajes[baldosaJugador]))		
    else:		
        print('¡Ha sido un empate!')		
		
    if not jugarDeNuevo():		
        break		
