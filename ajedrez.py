"""Juego de Ajedrez en consola"""
# Definición de las piezas y el tablero
PIEZAS = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙', '.': '.'
}

def tablero_inicial():
    """posicion inicial"""
    return [
        list("rnbqkbnr"),
        list("pppppppp"),
        list("........"),
        list("........"),
        list("........"),
        list("........"),
        list("PPPPPPPP"),
        list("RNBQKBNR"),
    ]

def imprimir_tablero(tablero):
    """imprime el tablero"""
    print("  a b c d e f g h")
    for i, fila in enumerate(tablero):
        print(8 - i, end=' ')
        for pieza in fila:
            print(PIEZAS.get(pieza, pieza), end=' ')
        print(8 - i)
    print("  a b c d e f g h")

def mover(tablero, origen, destino):
    """mueve la pieza de origen a destino"""
    x1, y1 = 8 - int(origen[1]), ord(origen[0]) - ord('a')
    x2, y2 = 8 - int(destino[1]), ord(destino[0]) - ord('a')
    pieza = tablero[x1][y1]
    if pieza == '.':
        print("No hay pieza en la casilla de origen.")
        return False
    tablero[x2][y2] = pieza
    tablero[x1][y1] = '.'
    return True

def main():
    """funcion principal"""
    tablero = tablero_inicial()
    turno_blancas = True
    while True:
        imprimir_tablero(tablero)
        jugador = "Blancas" if turno_blancas else "Negras"
        mov = input(f"{jugador} (ejemplo: e2 e4, o 'salir'): ").strip()
        if mov.lower() == 'salir':
            print("Juego terminado.")
            break
        try:
            origen, destino = mov.split()
            if mover(tablero, origen, destino):
                turno_blancas = not turno_blancas
        except (ValueError, IndexError):
            print("Movimiento inválido. Usa el formato 'e2 e4'.")

if __name__ == "__main__":
    main()
