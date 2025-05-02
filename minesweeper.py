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

            #gui objekte
            self.frame = None
            self.label = None
            self.button = None
   
    def __init__(self, shape, mines):
        self.rows, self.cols = shape
        self.shape = shape
        self.mines = mines
        self.matrix = [[self.Cell((i, j)) for j in range(self.cols)] for i in range(self.rows)]
        self.surrounding_offsets = [(0,1),(1,0),(1,1),(-1,0),(-1,1),(-1,-1),(1,-1),(0,-1),] #relative Koordinaten der Nachbarfelder einer Zelle
        self.spread_mines(mines)
        self.count_surrounding_mines()
        
    def spread_mines(self, mines):
        mines_put = 0
        while mines_put < mines:
            x =  rd.randint(0, self.rows-1)
            y =  rd.randint(0, self.cols-1)
            if not self.matrix[x][y].mine:
                self.matrix[x][y].mine = True
                mines_put += 1

    def count_surrounding_mines(self):
        for row in self.matrix:
            for cell in row:
                if not cell.mine:
                    for dx, dy in self.surrounding_offsets:
                        nx = cell.position[0] + dx
                        ny = cell.position[1] + dy
                        if 0 <= nx < self.rows and 0 <= ny < self.cols:
                            if self.matrix[nx][ny].mine:
                                cell.surrounding_mines += 1                        
 
                        
class GUI():

    def __init__(self, root, game):
        self.game = game
        self.root = root

        self.check_exit()

    def start_window(self):
        self.root.geometry('500x250')
        self.root.title('Minesweeper')

        #Button um das Spiel zu starten
        self.game_starter = tk.Button(master=self.root, height=10, width=20, text="Start\nGame", bg='gray', command=self.init_game)
        self.game_starter.pack(side='left', padx=50, pady=10)
        self.button_start_exist = True

        #Button um die Anleitung zu sehen
        self.tutorial_button = tk.Button(master=self.root, height=1, width=20, bg='gray', text="Tutorial", command=self.show_tutorial)
        self.tutorial_button.place(x=300, y=40)    
    
    def show_tutorial(self):
        tutorial_text="""
        exampel
        """
        tutorial_window = tk.Tk()
        tutorial_window.geometry("500x500")
        scrollbar = tk.Scrollbar(master=tutorial_window)
        text = tk.Text(master=tutorial_window, wrap='word', yscrollcommand=scrollbar.set)
        text.place(anchor='nw', relx=0, rely=0)
        text.insert("1.0", tutorial_text)
        text.config(state="disabled")
    

    def init_game(self):
        if self.button_start_exist:
            self.button_start_exist = False
            self.game_starter.destroy()
        self.root.title('Minesweeper')        

        #files
        self.currentscriptpath = Path(__file__).resolve().parent
        self.image_flag = tk.PhotoImage(file=self.currentscriptpath/"Data"/"flag.png")
        self.image_mine = tk.PhotoImage(file=self.currentscriptpath/"Data"/"mine.png")
        self.smiley = [
            tk.PhotoImage(file=self.currentscriptpath/"Data"/"smiley_yellow.png"),
            tk.PhotoImage(file=self.currentscriptpath/"Data"/"smiley_red.png"),
            tk.PhotoImage(file=self.currentscriptpath/"Data"/"smiley_green.png"),]

        self.gameFrame = tk.Frame(master=self.root)
        self.gameFrame.pack(fill='both', expand=True)
        
        self.create_guiboard(30,2)   # erzeuge GUI-Board, Parameter: Zellengröße, Zellenabstand
        
        self.topline()
        
        self.board_frame.pack(fill="x", expand=True, pady=10, padx=5)
        self.update_windowsize()

        self.check_exit()

    def start_screen(self):
        self.start_screen_frame = tk.Frame(master=self.root, bg='red')
        self.start_screen_frame.pack(fill='both', expand=True)
        self.start_screen_frame.lift()
    
    def create_guiboard(self, cellsize, padxy):
        self.cellsize = cellsize
        self.padxy = padxy

        self.board_frame = tk.Frame(self.gameFrame)
        #self.boardFrame.pack(fill='both', expand=True)

        for row in self.board.matrix:
            for cell in row:
                cell.frame = tk.Frame(master=self.board_frame, height=cellsize, width=self.cellsize, bg='gray')
                cell.frame.grid(row=cell.position[0], column=cell.position[1], padx=self.padxy, pady=self.padxy)
         
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
                           
    def guiboard_buttons(self):
        for row in self.board.matrix:
            for cell in row:
                cell.button = tk.Button(master=cell.frame, bg='gray', height=self.cellsize, width=self.cellsize)
                cell.button.place(relx=0.5, rely=0.5, anchor='center')
                cell.button.bind('<Button-1>', lambda event, cell=cell: self.open_field(event, cell))
                cell.button.bind('<Button-3>', lambda event, cell=cell: self.flag(event, cell))
                cell.label.bind('<Double-Button-1>', lambda event, cell=cell:self.chord(event, cell))
                         
    def topline(self):
        """oberer balken auf dem Spielbildschirm für Smileyknopf, Timer und Minenanzahl"""
        boardwidth = self.board.rows*(self.cellsize+self.padxy)
        self.topline_frame = tk.Frame(master=self.gameFrame, height=100, width=boardwidth,bg='lightgray')
        self.flags_left()
        
        """Smiley Button zum Restart des Spiels"""
        smiley_size = 80
        self.smiley_frame = tk.Frame(master=self.topline_frame, height=smiley_size, width=smiley_size,bg='red')
        self.smiley_button = tk.Button(master=self.smiley_frame, height=smiley_size, width=smiley_size, image=self.smiley[0], command=self.game.restart)
        self.smiley_frame.pack(side='top', padx=10)
        self.smiley_button.pack(expand=True)

        """Initialisierung des Timers"""
        self.timer_frame = tk.Frame(master=self.topline_frame, height=self.mines_left_size, width=self.mines_left_size)
        self.timer_label = tk.Label(master=self.timer_frame, height=self.mines_left_size, width=self.mines_left_size, text="0", font=("Arial", 14, "bold"))
        self.timer_label.place(anchor='center', relx=0.5, rely=0.5)
        self.timer_frame.place(x=boardwidth-self.mines_left_size, y=50-self.mines_left_size/2)
        self.timer_running = False
        #self.timer_update()

        self.topline_frame.pack(fill='x', padx=5)

    def flags_left(self):
        """Anzeige der Flaggen, die man theoretisch noch setzen muss"""
        self.mines_left = self.board.mines
        self.mines_left_size = 40
        self.mines_frame = tk.Frame(master=self.topline_frame, height=self.mines_left_size, width=self.mines_left_size,bg='red')
        self.mines_left_label = tk.Label(master=self.mines_frame, height=self.mines_left_size, width=self.mines_left_size, text=self.mines_left, font=("Arial", 14, "bold"), foreground='red')
        self.mines_left_label.place(relx=0.5, rely=0.5, anchor='center')
        self.mines_frame.place(x = 20, y = 50-self.mines_left_size/2)

    def timer_update(self):
        """Ändert den Timer um 1"""
        if self.timer_running:
            time = int(self.timer_label.cget('text'))
            time += 1
            self.timer_label.config(text=str(time))
            self.root.after(1000, self.timer_update)
     
    def open_field(self,event=None, cell=None):
        if not self.timer_running and self.game.gameactive:
            self.timer_running = True
            self.timer_update()

        if cell.mine:
            cell.label.config(bg='red')
        
        cell.revealed = True
        cell.label.place(relx=0.5, rely=0.5, anchor='center')
        cell.button.destroy()

        if self.game.gameactive:
            if cell.mine:
                self.game.lost()
            if cell.surrounding_mines == 0:
            
                self.chord(cell=cell)

            self.game.check_win()

    def open_all(self):
        for row in self.board.matrix:
            for cell in row:
                self.open_field(None, cell)

    def chord(self,event=None, cell=None):
        #self.open_field(cell=cell)
        for target in self.board.surrounding_offsets:
            nx, ny = cell.position[0]+target[0], cell.position[1] + target[1] 
            if 0 <= nx < self.board.rows and 0 <= ny < self.board.cols:
                neighbor = self.board.matrix[nx][ny]
                if not neighbor.revealed and not neighbor.flagged:
                    self.open_field(cell=neighbor)

    def flag(self,event=None, cell=None):
        if not cell.flagged: #setze Flagge
            cell.flagged = True
            cell.button.config(image=self.image_flag)
            self.mines_left -= 1
        else: #entferne flagge
            cell.flagged = False
            cell.button.config(image='')
            self.mines_left += 1
        self.mines_left_label.config(text=self.mines_left)

    def check_exit(self):
        self.root.bind('<Escape>',self.close_window)
    
    def close_window(self, event):
        self.root.quit()
        self.root.destroy()
    
    def screen_lost(self):
        self.smiley_button.config(image=self.smiley[1])
        self.open_all()
       

class Game():
    def __init__(self):
        self.root = tk.Tk()
        self.gui = GUI(self.root, self)

        self.gui.start_window()

    def start_game(self):
        self.gameactive = True

        self.gui.board = Board((10,10), 18)
        
                
        self.root.mainloop()

    def check_win(self):
        if self.gameactive:
            win = True
            for row in self.gui.board.matrix:
                for cell in row:
                    if not cell.mine:
                        if not cell.revealed:
                            win = False

            if win:
                self.win()

    def win(self):
        self.gui.smiley_button.config(image=self.gui.smiley[2])
        self.gameactive = False
        self.gui.timer_running = False

    def lost(self):
        self.gameactive = False
        self.gui.timer_running = False
        self.gui.screen_lost()
        
    def restart(self,event=None):
        self.gui.timer_running = False
        if self.root:
            self.root.destroy()

        self.__init__()
        self.start_game()

if __name__=='__main__':
    game = Game()
    game.start_game()