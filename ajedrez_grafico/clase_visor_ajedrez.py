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

    def mostrar(self):
        pygame.init()
        screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE))
        pygame.display.set_caption("Visor PGN con pygame")
        board = chess.Board()

        for i, mov in enumerate(self.movimientos, 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            board.push_san(mov)
            self.dibujar_tablero(screen)
            self.dibujar_piezas(screen, board)
            pygame.display.flip()
            pygame.time.wait(int(self.delay * 1000))

        # Espera hasta cerrar ventana
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
        pygame.quit()


# Ejemplo de uso
if __name__ == "__main__":
    pgn = """
1. e4 c6 2. d4 d5 3. Nc3 dxe4 4. Nxe4 Bf5 5. Ng3 Bg6 6. h4 h6 7. Nf3 Nd7 8. h5 Bh7 9. Bd3 Bxd3 10. Qxd3 e6 11. Bd2 Ngf6 12. O-O-O Be7 13. Ne4 Nxe4 14. Qxe4 Nf6 15. Qe2 Qd5 16. Kb1 Qe4 17. Qf1 O-O-O 18. Ne5 Rhf8 19. f3 Qd5 20. c4 Qxd4 21. Bc3 Qf4 22. Qf2 Rxd1+ 23.
"""
    movimientos = []
    for linea in pgn.strip().split('\n'):
        if not linea or linea[0] == '[':
            continue
        movimientos.extend([mov for mov in linea.strip().split()
                            if not mov[0].isdigit()
                            and mov not in ['1-0', '0-1', '1/2-1/2', '*']])
    visor = VisorPGN(movimientos)
    visor.mostrar()
