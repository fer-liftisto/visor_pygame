###FER###
from icecream import ic
import chess
import pygame

# Configuración
TILE_SIZE = 64
BOARD_SIZE = TILE_SIZE * 8
PIECE_PATH = {
    "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚", "bP": "♟",
    "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙"
} 

def dibujar_tablero(screen):
    colores = [pygame.Color(240, 217, 181), pygame.Color(181, 136, 99)]
    for fila in range(8):
        for col in range(8):
            color = colores[(fila + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                col*TILE_SIZE, fila*TILE_SIZE, TILE_SIZE, TILE_SIZE))


def dibujar_piezas(screen, board):
    font = pygame.font.SysFont("Segoe UI Symbol", 48)
    for sq in chess.SQUARES:
        pieza = board.piece_at(sq)
        if pieza:
            nombre = ('w' if pieza.color else 'b') + pieza.symbol().upper()
            simbolo = {
                "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚", "bP": "♟",
                "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙"
            }[nombre]
            fila = 7 - (sq // 8)
            col = sq % 8
            color = 'blue' if pieza.color else (119, 148, 85)   
            text = font.render(simbolo, True, color)
            screen.blit(text, (col * TILE_SIZE + 8, fila * TILE_SIZE + 4))


def mostrar_partida_pygame(movimientos, delay=1.0):
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Visor PGN con pygame")

    board = chess.Board()

    for i, mov in enumerate(movimientos, 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        board.push_san(mov) #
        dibujar_tablero(screen)
        dibujar_piezas(screen, board) #
        pygame.display.flip() # Actualiza la pantalla
        pygame.time.wait(int(delay * 1000))  # Espera entre jugadas

    # Espera hasta cerrar ventana
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
    pygame.quit()


def quitar(pgn, caracter1, caracter2):
    '''para quitatr parentesis'''
    paren = ''
    aux = False
    for i in pgn:
        if i == caracter1:
            aux = True
        if aux:
            paren += i
        if i == caracter2:
            aux = False
            pgn = pgn.replace(paren, '')
            paren = ''
    return pgn

# Ejemplo de uso
if __name__ == "__main__":
    pgn = """

[Evento "Partida relámpago puntuada"]
[Sitio " https://lichess.org/BNrT8FR2 "]
[Fecha "2024.09.16"]
[LIFTISTO blanco]
["jjdox" negro]
[Resultado "0-1"]
[Fecha UTC "2024.09.16"]
[Hora UTC "00:46:47"]
[Elo blanco "1582"]
[Elo negro "1621"]
[Diferencia de calificación de WhiteRating "-5"]
[Diferencia de calificación negra "+5"]
[Variante "Estándar"]
[Control de tiempo "300+0"]
[ECO "D45"]
[Introducción a la "Defensa Semieslava: Variante Normal"]
[Terminación "Normal"]
[Anotador " lichess.org "]

1. d4 { [%clk 0:05:00] } 1... e6 { [%clk 0:05:00] } 2. c4 { [%clk 0:04:58] } 2... d5 { [%clk 0:04:59] } 3. Cc3 { [%clk 0:04:56] } 3... Cf6 { [%clk 0:04:58] } 4. e3 { [%clk 0:04:55] } 4... c6 { [%clk 0:04:53] } 5. Cf3 { [%clk 0:04:53] } 5... Cbd7 { [%clk 0:04:52] } { D45 Defensa Semieslava: Variante Normal } 6. Ae2 { [%clk 0:04:52] } 6... Ad6  { [%clk 0:04:47] } 7. b3 { [%clk 0:04:50] } 7... e5 { [%clk 0:04:46] } 8. dxe5 { [%clk 0:04:46] } 8... Cxe5 { [%clk 0:04:45] } 9. OO { [%clk 0:04:42] } 9... Cxf3+ { [%clk 0:04:42] } 10. Axf3 { [%clk 0:04:40] } 10... Dc7 { [%clk 0:04:41] } 11. h3 { [%clk 0:04:33] } 11... OO { [%clk 0:04:38] } 12. cxd5 { [%clk 0:04:27] } 12... cxd5 { [%clk 0:04:34] } 13. Cxd5 { [%clk 0:04:25] } 13... Cxd5  { [%clk 0:04:32] } 14. Axd5 { [%clk 0:04:19] } 14... Td8 { [%clk 0:04:27] } 15. Df3 { [%clk 0:04:08] } 15... Ae6 { [%clk 0:03:49] } 16. Axe6 { [%clk 0:04:01] } 16... fxe6 { [%clk 0:03:48] } 17. Ab2 { [%clk 0:03:59] } 17... Tf8 { [%clk 0:03:43] } 18. Dg4 { [%clk 0:03:52] } 18... De7 { [%clk 0:03:34] } 19. Tad1 { [%clk 0:03:37] } 19... Tf7 { [%clk 0:03:22] } 20. Dd4 { [%clk 0:03:27] } 20... Ac5 { [%clk 0:03:16] } 21. De5 { [%clk 0:03:20] } 21... Taf8 { [%clk 0:03:09] } 22. Ad4 { [%clk 0:03:15] } 22... Ad6 { [%clk 0:03:06] } 23. Dg5 { [%clk 0:03:06] } 23... Dxg5 { [%clk 0:02:59] } { Las blancas se rinden. } 0-1

"""
    movimientos = []
    caracter1 = '{'
    caracter2 = '}' 
    for linea in pgn.strip().split('\n'):
        
        if not linea or linea[0] == '[':
            continue
        
        linea= quitar(linea, caracter1, caracter2)
        
        movimientos.extend([mov.replace('R','K')
                            .replace('C','N')
                            .replace('A','B')
                            .replace('D','Q')
                            .replace('T','R')
                            .replace('OOO', 'O-O-O')
                            .replace('OO', 'O-O')
                            for mov in linea.strip().split() 
                                            if not mov[0].isdigit() 
                                            and mov not in ['1-0', '0-1', '1/2-1/2', '*']])
                                                   
    ic(movimientos)
    mostrar_partida_pygame(movimientos)
