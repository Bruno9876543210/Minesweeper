import tkinter as tk
import numpy as np
import random as rd



class Board():
    """Board Klasse; verwalte 2D-Array von Zellen; bildet Core-Funktionalität
    Args:
        shape (tupel(int,int)): Größe Board
        mines (int): Anzahl Minen 
      
    Returns:
        _type_: _description_
    """
    
    class Cell():
        def __init__(self, pos):
            self.position = pos
            self.mine = False
            self.revealed = False
            self.surrounding_mines = 0
            self.surrounding = [(0,1),(1,0),(1,1),(-1,0),(-1,1),(-1,-1),(1,-1),(0,-1),] #relative Koordinaten aller Nachbarfelder

            #gui objekte
            self.frame = None
            self.label = None
            self.button = None

        def set_mine(self):
            self.mine = True        

        def __str__(self):
            if self.mine:
                return "X"
            else:
                return str(self.surrounding_mines)
    
    def __init__(self, shape, mines):
        self.matrix = np.full(shape, None)
        self.xlength = self.matrix.shape[0]
        self.ylength = self.matrix.shape[1]
        self.fill_matrix_with_cells()
        self.spreadmines(mines)
        self.count_surrounding_mines()
        
    def fill_matrix_with_cells(self):
        for i in range(self.xlength):
            for j in range(self.ylength):
                self.matrix[i,j] = self.Cell((i,j))
    
    def printmines(self):
        for i in range(self.xlength):
            print()
            for j in range(self.ylength):
                print(self.matrix[i,j],' ', end='')
                
        print()
    
    def spreadmines(self, mines):
        mines_put = 0
        while mines_put < mines:
            x =  rd.randint(0, self.matrix.shape[0]-1)
            y =  rd.randint(0, self.matrix.shape[0]-1)
            if not self.matrix[x,y].mine:
                self.matrix[x,y].set_mine()
                mines_put += 1

    def count_surrounding_mines(self):
        
        for i in range(self.xlength):
            for j in range(self.ylength):
                if not self.matrix[i,j].mine:
                    surrounding_mines = 0
                    for coords in self.matrix[i,j].surrounding:
                        exact_coordinate = (self.matrix[i,j].position[0]+coords[0]),(self.matrix[i,j].position[1]+coords[1])
                        if exact_coordinate[0] >=0 and exact_coordinate[0] < self.xlength and exact_coordinate[1] >=0 and exact_coordinate[1] < self.ylength:
                            if self.matrix[exact_coordinate].mine:
                                    surrounding_mines += 1
                        
                    self.matrix[i,j].surrounding_mines = surrounding_mines
                        
class GUI():
    def __init__(self, root, board, game):
        self.board = board
        self.game = game
        self.root = root
        self.root.title('Minesweeper')        


        self.create_guiboard(30,2)   # erzeuge GUI-Board, Parameter: Zellengröße, Zellenabstand
        
        self.check_exit()


    def create_guiboard(self, cellsize, padxy):
        self.cellsize = cellsize

        self.gameFrame = tk.Frame(master=self.root)
        self.gameFrame.pack(fill='both', expand=True)

        self.boardFrame = tk.Frame(self.gameFrame)
        self.boardFrame.pack(fill='both', expand=True)

        for i in range(self.board.xlength):
            for j in range(self.board.ylength):
                self.board.matrix[i,j].frame = tk.Frame(master=self.boardFrame, height=cellsize, width=self.cellsize, bg='gray')
                self.board.matrix[i,j].frame.grid(row=i, column=j, padx=padxy, pady=padxy)
         
        self.update_windowsize()
        self.guiboard_labels()
        self.guiboard_buttons()

    def update_windowsize(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.root.geometry(f"{width}x{height}")

    def guiboard_labels(self):
        for i in range(self.board.xlength):
            for j in range(self.board.ylength):
                self.board.matrix[i,j].label = tk.Label(master=self.board.matrix[i,j].frame, height=self.cellsize, width=self.cellsize)
                if self.board.matrix[i,j].mine:
                    self.board.matrix[i,j].label.config(text='X', bg='red')
                else:
                    colors = ['gray', 'blue', 'darkgreen', 'red', 'darkblue', 'violet', 'cyan', 'yellow', 'orange']
                    self.board.matrix[i,j].label.config(text=str(self.board.matrix[i,j].surrounding_mines),fg=colors[self.board.matrix[i,j].surrounding_mines], font=("Arial", 14, "bold"))
                    
                    
                #label.place(relx=0.5, rely=0.5, anchor='center')

    def guiboard_buttons(self):
        for i in range(self.board.xlength):
            for j in range (self.board.ylength):
                self.board.matrix[i,j].button = tk.Button(master=self.board.matrix[i,j].frame, bg='gray')
                self.board.matrix[i,j].button.place(relx=0.5, rely=0.5, anchor='center')
                self.board.matrix[i,j].button.bind('<Button-1>', lambda event, i=i, j=j: self.open_field(event, i, j))
                
    def open_field(self,event, i,j):
        self.board.matrix[i,j].revealed = True
        self.board.matrix[i,j].label.place(relx=0.5, rely=0.5, anchor='center')
        self.board.matrix[i,j].button.destroy()

        if game.gameactive:
            if self.board.matrix[i,j].mine:
                self.game.lost()

            
            self.game.check_win()

    def open_all(self):
        for i in range(self.board.xlength):
            for j in range(self.board.ylength):
                self.open_field(None, i,j)

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

        self.board = Board((5,5), 5)
        
        self.gui = GUI(self.root,self.board, self)
        self.root.mainloop()

    def check_win(self):
        if self.gameactive:
            win = True
            for i in range(self.board.xlength):
                for j in range(self.board.ylength):
                    if not self.board.matrix[i,j].mine:
                        if not self.board.matrix[i,j].revealed:
                            win = False

            if win:
                self.win()

    def win(self):
        print("You won")

    def lost(self):
        self.gameactive = False
        self.gui.screen_lost()
        
        for i in range(self.board.xlength):
            for j in range(self.board.ylength):
                if not self.board.matrix[i,j].revealed:
                    self.board.matrix[i,j].button.bind('<Button-1>', self.restart)
        self.root.bind('<Button-1>', self.restart)

    def restart(self,event):
        self.root.destroy()
        self.start()

if __name__=='__main__':
    game = Game()
    game.start()