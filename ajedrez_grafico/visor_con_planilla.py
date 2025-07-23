from icecream import ic
import chess
import chess.pgn
import tkinter as tk
import io


class ChessViewer(tk.Tk):
    def __init__(self, pgn_text):
        super().__init__()
        self.title("Visor de Partida de Ajedrez")
        self.geometry("700x650")
        self.pgn = chess.pgn.read_game(io.StringIO(pgn_text))
        self.moves = [move for move in self.pgn.mainline_moves()]
        self.board = self.pgn.board()
        self.move_index = 0

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(pady=10)

        # Tablero
        self.canvas = tk.Canvas(main_frame, width=400, height=400)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10)

        # Planilla de ajedrez (movimientos)
        self.planilla = tk.Text(main_frame, width=20,
                                height=25, font=("Consolas", 12))
        self.planilla.grid(row=0, column=1, padx=10)
        self.planilla.config(state=tk.DISABLED)

        # Info y botones
        self.info = tk.Label(main_frame, text="", font=("Arial", 12))
        self.info.grid(row=1, column=1, pady=10)
        btn_frame = tk.Frame(self)
        btn_frame.pack()
        self.prev_btn = tk.Button(btn_frame, text="⏪", command=self.prev_move, font=("Arial", 20), width=4, height=2)
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        self.next_btn = tk.Button(btn_frame, text="⏩", command=self.next_move, font=("Arial", 20), width=4, height=2)
        self.next_btn.pack(side=tk.LEFT, padx=10)

        self.bind("<Left>", lambda e: self.prev_move())
        self.bind("<Right>", lambda e: self.next_move())
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_canvas_click)
        self.draw_board()
        self.update_info()
        self.update_planilla()

    def draw_board(self):
        self.canvas.delete("all")
        size = 50
        colors = ["#f0d9b5", "#b58863"]
        for r in range(8):
            for c in range(8):
                x0, y0 = c * size, r * size
                x1, y1 = x0 + size, y0 + size
                color = colors[(r + c) % 2]
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=color, outline="")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                x = col * size + size // 2
                y = row * size + size // 2
                self.canvas.create_text(
                    x, y, text=self.piece_unicode(piece), font=("Arial", 32))

    def piece_unicode(self, piece):
        symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        return symbols[piece.symbol()]

    def update_info(self):
        move_text = f"Movimiento {self.move_index}/{len(self.moves)}"
        self.info.config(text=move_text)

    def update_planilla(self):
        self.planilla.config(state=tk.NORMAL)
        self.planilla.delete(1.0, tk.END)
        board = self.pgn.board()
        texto = ""
        indices = []
        for i, move in enumerate(self.moves):
            if i % 2 == 0:
                texto += f"{(i//2)+1}. "
            start_idx = len(texto)
            texto += board.san(move) + " "
            end_idx = len(texto)
            indices.append((start_idx, end_idx))
            board.push(move)
            if i % 2 == 1:
                texto += "\n"
        self.planilla.insert(tk.END, texto)
        self.planilla.tag_remove("actual", "1.0", tk.END)
        if self.move_index > 0:
            ini, fin = indices[self.move_index-1]
            ini_tk = f"1.0+{ini}c"
            fin_tk = f"1.0+{fin}c"
            self.planilla.tag_add("actual", ini_tk, fin_tk)
            self.planilla.tag_config("actual", background="green", foreground="white")
            # Scroll automático al movimiento actual
            self.planilla.see(ini_tk)
        self.planilla.config(state=tk.DISABLED)

    def next_move(self):
        if self.move_index < len(self.moves):
            self.board.push(self.moves[self.move_index])
            self.move_index += 1
            self.draw_board()
            self.update_info()
            self.update_planilla()

    def prev_move(self):
        if self.move_index > 0:
            self.board.pop()
            self.move_index -= 1
            self.draw_board()
            self.update_info()
            self.update_planilla()

    def on_canvas_click(self, event):
        if event.num == 1:
            self.next_move()
        elif event.num == 3:
            self.prev_move()


def traducir_movimientos_pgn(pgn):
    # Diccionario de traducción de piezas
    piezas = {
        'C': 'N',  # Caballo -> Knight
        'A': 'B',  # Alfil -> Bishop
        'D': 'Q',  # Dama -> Queen
        'T': 'R',  # Torre -> Rook
        'O-O-O': 'O-O-O',  # Enroque largo
        'O-O': 'O-O',      # Enroque corto
        'OO': 'O-O',       # Enroque corto (algunas bases usan OO)
    }
    # Reemplaza enroques primero
    pgn = re.sub(r'\bOOO\b', 'O-O-O', pgn)
    pgn = re.sub(r'\bOO\b', 'O-O', pgn)
    # Reemplaza piezas
    for esp, eng in piezas.items():
        # Solo reemplaza fuera de corchetes (no en metadatos)
        pgn = re.sub(r'(?<=\s)' + esp, eng, pgn)
        pgn = re.sub(r'^' + esp, eng, pgn, flags=re.MULTILINE)
    return pgn


if __name__ == "__main__":
    import re
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
    pgn_traducido = traducir_movimientos_pgn(pgn)
    ChessViewer(pgn_traducido).mainloop()
