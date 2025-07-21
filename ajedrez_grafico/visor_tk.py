from  icecream import ic
import re
import io
import tkinter as tk

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
import chess.pgn

class ChessViewer(tk.Tk):
    def __init__(self, pgn_text):
        super().__init__()
        self.title("Visor de Partida de Ajedrez")
        self.geometry("500x550")
        self.pgn = chess.pgn.read_game(io.StringIO(pgn_text))
        self.moves = [move for move in self.pgn.mainline_moves()]
        self.board = self.pgn.board()
        self.move_index = 0

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(pady=20)
        self.info = tk.Label(self, text="", font=("Arial", 12))
        self.info.pack()
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()
        self.prev_btn = tk.Button(self.btn_frame, text="⏪", command=self.prev_move)
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        self.next_btn = tk.Button(self.btn_frame, text="⏩", command=self.next_move)
        self.next_btn.pack(side=tk.LEFT, padx=10)

        self.bind("<Left>", lambda e: self.prev_move())
        self.bind("<Right>", lambda e: self.next_move())
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_board()
        self.update_info()

    def draw_board(self):
        self.canvas.delete("all")
        size = 50
        colors = ["#f0d9b5", "#b58863"]
        for r in range(8):
            for c in range(8):
                x0, y0 = c * size, r * size
                x1, y1 = x0 + size, y0 + size
                color = colors[(r + c) % 2]
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                x = col * size + size // 2
                y = row * size + size // 2
                self.canvas.create_text(x, y, text=self.piece_unicode(piece), font=("Arial", 32))

    def piece_unicode(self, piece):
        symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        return symbols[piece.symbol()]

    def update_info(self):
        move_text = f"Movimiento {self.move_index}/{len(self.moves)}"
        self.info.config(text=move_text)

    def next_move(self):
        if self.move_index < len(self.moves):
            self.board.push(self.moves[self.move_index])
            self.move_index += 1
            self.draw_board()
            self.update_info()

    def prev_move(self):
        if self.move_index > 0:
            self.board.pop()
            self.move_index -= 1
            self.draw_board()
            self.update_info()

    def on_canvas_click(self, event):
        # Avanza al siguiente movimiento con clic izquierdo, retrocede con derecho
        if event.num == 1:
            self.next_move()
        elif event.num == 3:
            self.prev_move()


def traduce_replace(f):
    '''Traduce de sp a uk'''
    # '♟♜♞♝♛♚' #
    f = f.replace('R', 'K')
    f = f.replace('T', 'R')
    f = f.replace('C', 'N')
    f = f.replace('A', 'B')
    f = f.replace('D', 'Q')
    f = f.replace('OOO', 'O-O-O')
    f = f.replace('OO', 'O-O')
    return f

if __name__ == "__main__":
    movimientos= []
    for linea in pgn.strip().split('\n'):

        if not linea or linea[0] == '[':
            continue
        busca = r'[TCADR]?[a-h]?[1-8]?x?[a-h][1-8]=?[TCAQ]?|O-O-O|O-O|OOO|OO'
        planilla1 = re.findall(busca, linea)
        ic(planilla1)
        for movi in planilla1:
            movimientos.append(traduce_replace(movi))
        ic(movimientos)
        
    ic(' '.join(movimientos))
    ChessViewer(' '.join(movimientos)).mainloop()