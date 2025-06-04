import tkinter as tk
import numpy as np
import random as rd
from pathlib import Path
from tkinter import messagebox



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

        self.presettings()

        self.check_exit()

    def presettings(self):
        """Standartwerte für die Variablen in den Einstellungen"""

        
        self.starthelp_activated = self.game.presettings[0]
        self.quantity_mines = self.game.presettings[1]

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

        #Button um zu den Einstellungen zu kommen
        self.settings_button = tk.Button(master=self.root, height=1, width=20, bg='gray', text="Settings", command=self.show_settings_window)
        self.settings_button.place(x=300, y=100)  

        #Button für den Projektablauf
        self.doku_button = tk.Button(master=self.root, height=1, width=20, text="Dokumentation", bg='gray', command=self.show_doku)
        self.doku_button.place(x=300, y=160)
    
    def show_doku(self):
        doku_text = """
        Die Idee für mein Projekt hatte ich in den Faschingsferien im Skiurlaub.
        Auf den Gondelfahrten habe ich mir dort bereits im Kopf einen recht detailierten Plan für das Programm gemacht.
        Daher die Programmierung dann in den ersten Unterrichtsstunden auch besonders schnell.

        Angefangen habe ich mit der "Core Logik", noch ohne Grafische Oberfläche.
        Dazu habe ich die Board- und die Cell-Klasse und das damit verbundene Array für das Spielfeld angelegt.
        Nun habe ich eine Funktion geschrieben, die dort zufällig "Minen verteilt" und anschließend eine,
        mit welcher für jede Zelle durch alle Nachbarfelder iteriert wird und dabei die Anzahl der Nachbarminen gezählt wird.
        Damit war das Grundsätzliche Spielfeld auch schon quasi fertig.
        Dieses konnte in den frühen Versionen jedoch nur über den print() Befehl angezeigt werden.

        Im nächsten Schritt habe ich dann die GUI-Klasse angelegt und das Spielfeld nun auch als grafische Oberfläche programmiert.
        Dazu habe ich für jede Zelle einen Button angelegt, der beim Anklicken verschwindet und die Zahl darunter freigibt.
        Danach habe ich das Verlieren eingebaut, indem das Spiel durch das Aufdecken einer Mine beendet wird.
        Sobald man alle Felder ohne Mine geöffnet hat, hat man das Spiel gewonnen.
        Diese Aufgaben des anschließenden Neustarts oder dem Beenden des Spiels habe ich in die "Game Klasse" ausgelagert.

        Bis jetzt musste man sich immer merken, wo man eine Mine vermutete, daher habe ich, wie im Originalspiel auch,
        die das Flaggensetzen ermöglicht.

        Damit Flaggen und Minen nicht mehr mit "F" und "X" als Text angezeigt wurden, habe ich anschließend Grafiken dafür implementiert.

        Außerdem wollte ich einen richtigen Restart-Knopf. Zuvor konnte man nach dem beendeten Spiel (Sieg oder Niederlage) mit einem beliebigen Klick neustarten.
        Das erlaubte einem allerdings nicht, eine laufende Runde zu unterbrechen, ohne das komplette Programm neuzustarten.
        In den Restart-Knopf habe ich auch gleich noch eine Anzeige des Spielstatuses eingebaut.
        So ist der sehr prominent plazierte Smiley-Button entstanden.
        
        Um das Spiel spannender zu gestalten, habe ich mich anschließend entschieden, einen Timer einzubauen, damit man auf Zeit spielen kann.

        Desweiteren habe ich eine Anzeige programmiert, wie viele Minen noch übrig sind, damit man daraus eventuell Schlüsse über ihre Verteilung ziehen kann.

        Soweit hat das Spiel bereits sehr gut funktioniert und auch Spaß zu spielen gemacht, jedoch fehlte noch ein wichtiger Schritt:
        Um die Projektanforderungen mit den Erklärungstexten zu erfüllen, sowie Einstellungen zu ermölichen, brauchte ich ein Hauptmenü.
        Dazu habe ich das selbe Fenster wie das Spiel verwendet, jedoch einen anderen Hauptframe angezeit.
        Die einzelnen Knöpfen habe ich mit dem Öffnen von den verschiedenen Unterfenstern verbunden, die beispielsweise diesen Text hier anzeigen.

        Das Spiel hatte aber noch ein Problem:
        Um das Spiel zu beginnen, musste man immer raten und es konnte teilweise lange dauern, bis man wirklich spielen konnte.
        Daher habe ich immer die erste 0, also ein Feld ohne Mine in einem Nachbarfeld, grün markieren lassen.
        Wenn man es lieber auf die "Harte Tour" probieren möchte, kann man dieses Feature aber auch in den Einstellungen deaktivieren.
        """
        if not hasattr(self, "doku_window") or not tk.Toplevel.winfo_exists(self.doku_window):
                self.doku_window = tk.Toplevel()
                self.doku_window.title("Dokumentation")
                self.doku_window.geometry("575x500")
                scrollbar = tk.Scrollbar(master=self.doku_window)
                text = tk.Text(master=self.doku_window, wrap='word', yscrollcommand=scrollbar.set)
                text.place(anchor='nw', relx=0, rely=0)
                text.insert("1.0", doku_text)
                text.config(state="disabled")
        else: self.doku_window.destroy()

    def show_settings_window(self):
        if not hasattr(self, "settings_window") or not tk.Toplevel.winfo_exists(self.settings_window):
            self.settings_window = tk.Toplevel()
            self.settings_window.title("Settings")
            self.settings_window.geometry("500x400")

            #Apply-Button
            self.apply_button = tk.Button(master=self.settings_window, height=2, width=5, text='Apply', command=self.apply_settings, font=("Arial", 10, "bold"))
            self.apply_button.pack(side='top', pady=1)

            #Button zur Aktivierung der Starthilfe
            self.checkbutton_starthelp_var = tk.BooleanVar(value=self.starthelp_activated)
            self.checkbutton_starthelp = tk.Checkbutton(master=self.settings_window, text="Zeige bei Spielbeginn ein Feld mit 0 an", offvalue=False, onvalue=True, variable=self.checkbutton_starthelp_var, command=self.apply_settings)
            self.checkbutton_starthelp.pack(side='top')

            #Entry Anzahl Minen
            self.quantity_mines_frame = tk.Frame(master=self.settings_window, height=2, width=10, bg='white')
            self.quantity_mines_frame.pack(side='top', pady=1)
            self.quantity_mines_label = tk.Label(master=self.quantity_mines_frame, height=2, width=50, bg='white', text="Mine quantity: ", fg='black')
            self.quantity_mines_label.pack(side='left')
            self.quantity_mines_entry = tk.Entry(master=self.quantity_mines_frame, bg='grey')
            self.quantity_mines_entry.insert(0,self.quantity_mines)
            self.quantity_mines_entry.pack(side='right', padx=1)
            

        else:
            self.apply_settings()
            self.settings_window.destroy()

    def apply_settings(self):
        self.starthelp_activated = self.checkbutton_starthelp_var.get()

        try:
            if 0 < int(self.quantity_mines_entry.get()) < 100:
                self.quantity_mines = int(self.quantity_mines_entry.get())
                print(self.quantity_mines)
            else: messagebox.showerror("Error", "This mine quantity is not possible!")
        except: messagebox.showerror("Error", "Input makes no sense!")

        
        self.game.presettings = [self.starthelp_activated, self.quantity_mines]
        

    def show_tutorial(self):
        tutorial_text="""
        Das Ziel des Spiels "Minesweeper" ist es, ein Minenfeld freizuräumen, ohne auf eine Mine zu stoßen.
        Dazu gräbt man immer die Felder auf, von welchen man weiß, dass sie sicher sind.
        Sollte man versehentlich doch auf eine Mine treffen explodiert diese und das Spiel ist vorbei.

        Wenn man ein freies Feld aufgedeckt hat, wird automatisch ein Radar plaziert,
        der die Minen in den umliegenden Feldern (auch diagonal) zählt.
        Nur mit diesen Informationen lässt sich im Spielverlauf meist nur mithilfe von Logik das Gesamte Spielfeld freiräumen.
        Ein Feld, von welchem du weißt, dass eine Mine darunter verborgen liegt, kannst du mit einer Flagge markieren.
        Diese ist nur eine Markierung für dich und wird nicht kontrolliert. Sollte sie falsch gesetzt sein,
        führt es jedoch wahrscheinlich in den nächsten paar Zügen zur Niederlage.

        Oben links in der Ecke sieht man zu Beginn die Anzahl der vergrabenen Minen.
        Wenn du eine Flagge setzt, wird Eins abgezogen, wenn also alle Flaggen richtig gesetzt sind, weißt du, wie viele noch fehlen.
        Sollte die Zahl negativ werden, hast du einen Fehler gemacht...

        Der Smiley oben in der Mitte ist der Restart Knopf des Spiels und zeigt gleichzeitig noch den Status des Spiels an:
        Ist er gelb, ist das Spiel im Gange, bei Grüner Farbe hast du gewonnen (Alle freien Felder geöffnet), bei Niederlage wird er Rot.
        Wenn man ihn anklickt, kommt man wieder ins Hauptmenü.

        Rechts daneben findet sich der Timer.
        Damit kannst du sehen, wie lange du für das Spiel gebraucht hast und persönliche Rekorde brechen!

        Um Zeit zu sparen gibt es eine Methode in Minesweeper, die sich Chording nennt:
        Wenn man alle Minen um ein Feld mit einer Flagge markiert hat (Anzahl Flaggen stimmt mit der Zahl im Feld überein),
        kann man mit einem Doppelklick auf dieses Feld alle anderen Nachbarfelder aufdecken.
        Wenn um ein Feld keine einzige Mine zu finden ist, werden automatisch alle Nachbarfelder geöffnet.

        Steuerung:
        Feld ausgraben: Linksklick auf das Feld
        Flagge setzen: Rechtsklick auf das Feld
        Chording: Doppelklick auf das Feld

        Bei Interesse findet man genauere Anleitungen zu Spielweise und Taktiken im Internet.
        """
        if not hasattr(self, "tutorial_window") or not tk.Toplevel.winfo_exists(self.tutorial_window):
                self.tutorial_window = tk.Toplevel()
                self.tutorial_window.title("Tutorial")
                self.tutorial_window.geometry("575x500")
                scrollbar = tk.Scrollbar(master=self.tutorial_window)
                text = tk.Text(master=self.tutorial_window, wrap='word', yscrollcommand=scrollbar.set)
                text.place(anchor='nw', relx=0, rely=0)
                text.insert("1.0", tutorial_text)
                text.config(state="disabled")
        else: self.tutorial_window.destroy()
    
    def init_game(self):
        self.board = Board((10,10), self.quantity_mines)

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
        self.starthelp()

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
        """oberer balken auf dem Spielbildschirm für Restart, Timer und Minenanzahl"""
        boardwidth = self.board.rows*(self.cellsize+self.padxy)
        self.topline_frame = tk.Frame(master=self.gameFrame, height=100, width=boardwidth,bg='lightgray')
        self.flags_left()
        
        #Smiley Button zum Restart des Spiels
        smiley_size = 80
        self.smiley_frame = tk.Frame(master=self.topline_frame, height=smiley_size, width=smiley_size,bg='red')
        self.smiley_button = tk.Button(master=self.smiley_frame, height=smiley_size, width=smiley_size, image=self.smiley[0], command=self.game.restart)
        self.smiley_frame.pack(side='top', padx=10)
        self.smiley_button.pack(expand=True)

        #Initialisierung des Timers
        self.timer_frame = tk.Frame(master=self.topline_frame, height=self.mines_left_size, width=self.mines_left_size)
        self.timer_label = tk.Label(master=self.timer_frame, height=self.mines_left_size, width=self.mines_left_size, text="0", font=("Arial", 14, "bold"))
        self.timer_label.place(anchor='center', relx=0.5, rely=0.5)
        self.timer_frame.place(x=boardwidth-self.mines_left_size, y=50-self.mines_left_size/2)
        self.timer_running = False

        # Hauptmenü button
        # self.button_back_frame = tk.Frame(master=self.topline_frame, height=2, width=smiley_size, bg='gray')
        # self.button_back = tk.Button(master=self.topline_frame, height=2, width=5, text="Back", command=self.game.restart)
        # self.button_back_frame.pack(side='top', padx=1, pady=0)
        # self.button_back.pack(expand=True)

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

    def starthelp(self):
        if self.starthelp_activated:
            for row in self.board.matrix:
                for cell in row:
                    if cell.surrounding_mines == 0 and not cell.mine:
                        cell.button.config(bg='green')
                        return

    def check_exit(self):
        self.root.bind('<Escape>',self.close_window)
    
    def close_window(self, event):
        if hasattr('self', self.tutorial_window) and self.tutorial_window: self.tutorial_window.destroy()
        if hasattr('self', self.settings_window) and self.settings_window: self.settings_window.destroy()
        if hasattr('self', self.doku_window) and self.doku_window: self.doku_window.destroy()
        self.timer_running = False
        self.root.quit()
        self.root.destroy()
            
    def screen_lost(self):
        self.smiley_button.config(image=self.smiley[1])
        self.open_all()
       

class Game():
    def __init__(self, presettings=[True, 18]):
        self.root = tk.Tk()
        self.presettings = presettings
        self.gui = GUI(self.root, self)

        self.gui.start_window()

    def start_game(self):
        self.gameactive = True    
                
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
        if hasattr(self.gui, "tutorial_window") and self.gui.tutorial_window:
            self.gui.tutorial_window.destroy()
        if hasattr(self.gui, "settings_window") and self.gui.settings_window:
            self.gui.settings_window.destroy()
        if self.root: self.root.destroy()
        

        self.__init__(presettings=self.presettings)
        self.start_game()

if __name__=='__main__':
    game = Game()
    game.start_game()