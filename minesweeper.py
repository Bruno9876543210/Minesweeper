import tkinter as tk
import numpy as np
import random as rd
from pathlib import Path



class Board():
    """Board Klasse; verwalte 2D-Array von Zellen; bildet Core-Funktionalität
    Args:
        shape (tupel(int,int)): Größe Board
        mines (int): Anzahl Minen 
      
    Returns:
        _type_: _description_
    """
    
    class Cell():
        """Einzelne Zelle; gemeinsamer speicherort für alle Zellbezogenen variablen
        Args:
            pos (tupel(int,int)): Koordinaten der Zelle in der Matrix
        """
        def __init__(self, pos):
            self.position = pos
            self.mine = False
            self.revealed = False
            self.flagged = False
            self.surrounding_mines = 0
            self.surrounding_offsets = [(0,1),(1,0),(1,1),(-1,0),(-1,1),(-1,-1),(1,-1),(0,-1),] #relative Koordinaten aller Nachbarfelder

            #gui objekte
            self.frame = None
            self.label = None
            self.button = None

        # def set_mine(self):
        #     self.mine = True        

        def __str__(self):
            if self.mine:
                return "X"
            else:
                return str(self.surrounding_mines)
    
    def __init__(self, shape, mines):
        self.shape =  shape
        self.matrix = [[self.Cell((j,i)) for i in range(self.shape[0])] for j in range(self.shape[1])]
        self.spread_mines(mines)
        self.count_surrounding_mines()
     
    def printmines(self):
        for row in self.matrix:
            print()
            for cell in row:
                print(cell,' ', end='')
                
        print()
    
    def spread_mines(self, mines):
        mines_put = 0
        while mines_put < mines:
            x =  rd.randint(0, self.shape[0]-1)
            y =  rd.randint(0, self.shape[1]-1)
            if not self.matrix[x][y].mine:
                self.matrix[x][y].mine = True
                mines_put += 1

    def count_surrounding_mines(self):
        
        for row in self.matrix:
            for cell in row:
                if not cell.mine:
                    for dx, dy in cell.surrounding_offsets:
                        nx = cell.position[0] + dx
                        ny = cell.position[1] + dy
                        if 0 <= nx < self.shape[0] and 0 <= ny < self.shape[1]:
                            if self.matrix[nx][ny].mine:
                                cell.surrounding_mines += 1                        
 
                        
class GUI():
    def __init__(self, root, board, game):
        self.board = board
        self.game = game
        self.root = root
        self.root.title('Minesweeper')        

        #files
        self.currentscriptpath = Path(__file__).resolve().parent
        self.image_flag = tk.PhotoImage(file=self.currentscriptpath/"Data"/"flag.png")
        self.image_mine = tk.PhotoImage(file=self.currentscriptpath/"Data"/"mine.png")

        self.create_guiboard(30,2)   # erzeuge GUI-Board, Parameter: Zellengröße, Zellenabstand
        
        self.check_exit()


    def create_guiboard(self, cellsize, padxy):
        self.cellsize = cellsize

        self.gameFrame = tk.Frame(master=self.root)
        self.gameFrame.pack(fill='both', expand=True)

        self.boardFrame = tk.Frame(self.gameFrame)
        self.boardFrame.pack(fill='both', expand=True)

        for row in self.board.matrix:
            for cell in row:
                cell.frame = tk.Frame(master=self.boardFrame, height=cellsize, width=self.cellsize, bg='gray')
                cell.frame.grid(row=cell.position[0], column=cell.position[1], padx=padxy, pady=padxy)
         
        self.update_windowsize()
        self.guiboard_labels()
        self.guiboard_buttons()

    def update_windowsize(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.root.geometry(f"{width}x{height}")

    def guiboard_labels(self):
        for row in self.board.matrix:
            for cell in row:
                cell.label = tk.Label(master=cell.frame, height=self.cellsize, width=self.cellsize)
                if cell.mine:
                    cell.label.config(image=self.image_mine, text='X')
                else:
                    colors = ['gray', 'blue', 'darkgreen', 'red', 'darkblue', 'violet', 'cyan', 'yellow', 'orange']
                    cell.label.config(text=str(cell.surrounding_mines),fg=colors[cell.surrounding_mines], font=("Arial", 14, "bold"))
                    
                    
                #label.place(relx=0.5, rely=0.5, anchor='center')

    def guiboard_buttons(self):
        for row in self.board.matrix:
            for cell in row:
                cell.button = tk.Button(master=cell.frame, bg='gray')
                cell.button.place(relx=0.5, rely=0.5, anchor='center')
                cell.button.bind('<Button-1>', lambda event, cell=cell: self.open_field(event, cell))
                cell.button.bind('<Button-3>', lambda event, cell=cell: self.flag(event, cell))
                
    def open_field(self,event, cell):
        if cell.mine:
            cell.label.config(bg='red')
        
        cell.revealed = True
        cell.label.place(relx=0.5, rely=0.5, anchor='center')
        cell.button.destroy()

        if self.game.gameactive:
            if cell.mine:
                self.game.lost()

            self.game.check_win()

    def open_all(self):
        for row in self.board.matrix:
            for cell in row:
                self.open_field(None, cell)

    def flag(self,event=None, cell=None):
        if not cell.flagged: #setze Flagge
            cell.flagged = True
            cell.button.config(image=self.image_flag)
        else: #entferne flagge
            cell.flagged = False
            cell.button.config(image='')

    def check_exit(self):
        self.root.bind('<Escape>',self.close_window)
    
    def close_window(self, event):
        self.root.quit()
        self.root.destroy()
    
    def screen_lost(self):
        self.open_all()

class Game():
    def start(self):
        self.gameactive = True
        self.root = tk.Tk()

        self.board = Board((10,10), 10)
        
        self.gui = GUI(self.root,self.board, self)
        
        self.root.mainloop()

    def check_win(self):
        if self.gameactive:
            win = True
            for row in self.board.matrix:
                for cell in row:
                    if not cell.mine:
                        if not cell.revealed:
                            win = False

            if win:
                self.win()

    def win(self):
        print("You won")

    def lost(self):
        self.gameactive = False
        self.gui.screen_lost()
        
        for row in self.board.matrix:
            for cell in row:
                if not cell.revealed:
                    cell.button.bind('<Button-1>', self.restart)
        self.root.bind('<Button-1>', self.restart)

    def restart(self,event=None):
        if self.root:
            self.root.destroy()
        self.start()

if __name__=='__main__':
    game = Game()
    game.start()