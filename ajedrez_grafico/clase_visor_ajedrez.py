###FER###
from icecream import ic 
import chess
import pygame


class VisorPGN:
    TILE_SIZE = 64
    BOARD_SIZE = TILE_SIZE * 8
    PIECE_SYMBOLS = {
        "bR": "♜", "bN": "♞", "bB": "♝", "bQ": "♛", "bK": "♚", "bP": "♟",
        "wR": "♖", "wN": "♘", "wB": "♗", "wQ": "♕", "wK": "♔", "wP": "♙"
    }

    def __init__(self, movimientos, delay=1.0):
        self.movimientos = movimientos
        self.delay = delay

    def dibujar_tablero(self, screen):
        colores = [pygame.Color(240, 217, 181), pygame.Color(181, 136, 99)]
        for fila in range(8):
            for col in range(8):
                color = colores[(fila + col) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(
                    col*self.TILE_SIZE, fila*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))

    def dibujar_piezas(self, screen, board):
        font = pygame.font.SysFont("Segoe UI Symbol", 48)
        for sq in chess.SQUARES:
            pieza = board.piece_at(sq)
            if pieza:
                nombre = ('w' if pieza.color else 'b') + pieza.symbol().upper()
                simbolo = self.PIECE_SYMBOLS[nombre]
                fila = 7 - (sq // 8)
                col = sq % 8
                color = 'blue' if pieza.color else (0, 0, 0)
                text = font.render(simbolo, True, color)
                screen.blit(text, (col * self.TILE_SIZE +
                            8, fila * self.TILE_SIZE + 4))

    def mostrar_planilla(self):
        # Crea una ventana de texto con la planilla de movimientos
        pygame.init()
        font = pygame.font.SysFont("Consolas", 24)
        width, height = 400, 600
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Planilla de ajedrez")
        running = True

        # Genera la planilla en formato tradicional
        texto = ""
        board = chess.Board()
        for i, mov in enumerate(self.movimientos):
            if i % 2 == 0:
                texto += f"{(i//2)+1}. "
            texto += mov + " "
            board.push_san(mov)
            if i % 2 == 1:
                texto += "\n"

        # Renderiza la planilla
        lines = texto.split('\n')
        while running:
            screen.fill((255, 255, 255))
            for idx, line in enumerate(lines):
                img = font.render(line, True, (0, 0, 0))
                screen.blit(img, (10, 10 + idx * 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        pygame.quit()

    def mostrar(self):
        pygame.init()
        # Nueva ventana más ancha para tablero + planilla
        screen = pygame.display.set_mode((self.BOARD_SIZE + 300, self.BOARD_SIZE))
        pygame.display.set_caption("Visor PGN con planilla")
        board = chess.Board()
        font = pygame.font.SysFont("Consolas", 24)

        # Prepara la planilla de movimientos
        texto = ""
        for i, mov in enumerate(self.movimientos):
            if i % 2 == 0:
                texto += f"{(i//2)+1}. "
            texto += mov + " "
            if i % 2 == 1:
                texto += "\n"
        lines = texto.split('\n')

        for i, mov in enumerate(self.movimientos, 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            board.push_san(mov)
            self.dibujar_tablero(screen)
            self.dibujar_piezas(screen, board)
            screen.fill((255, 255, 255), rect=pygame.Rect(self.BOARD_SIZE, 0, 300, self.BOARD_SIZE))
            jugada_actual = (i-1)//2
            max_lines = self.BOARD_SIZE // 30 - 1
            start_line = max(0, jugada_actual - max_lines//2)
            end_line = min(len(lines), start_line + max_lines)
            for idx in range(start_line, end_line):
                line = lines[idx]
                # Divide la línea en número de jugada, movimiento blanco y movimiento negro
                partes = line.strip().split()
                x_base = self.BOARD_SIZE + 10
                y_base = 10 + (idx-start_line) * 30
                x = x_base
                # Número de jugada
                if partes:
                    img = font.render(partes[0], True, (0, 0, 0))
                    screen.blit(img, (x, y_base))
                    x += img.get_width() + 10
                # Movimiento blanco
                if len(partes) > 1:
                    color = (255, 0, 0) if (idx == jugada_actual and i % 2 == 1) else (0, 0, 0)
                    img = font.render(partes[1], True, color)
                    screen.blit(img, (x, y_base))
                    x += img.get_width() + 10
                # Movimiento negro
                if len(partes) > 2:
                    color = (255, 0, 0) if (idx == jugada_actual and i % 2 == 0) else (0, 0, 0)
                    img = font.render(partes[2], True, color)
                    screen.blit(img, (x, y_base))
            pygame.display.flip()
            pygame.time.wait(int(self.delay * 1000))

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
        linea = quitar(linea, caracter1, caracter2)
        movimientos.extend([mov.replace('R', 'K')
                            .replace('C', 'N')
                            .replace('A', 'B')
                            .replace('D', 'Q')
                            .replace('T', 'R')
                            .replace('OOO', 'O-O-O')
                            .replace('OO', 'O-O')
                                 for mov in linea.strip().split()
                                            if not mov[0].isdigit()
                                            and mov not in ['1-0', '0-1', '1/2-1/2', '*']])
    visor = VisorPGN(movimientos)
    ic(movimientos)
    visor.mostrar()
