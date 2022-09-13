from pythonsweeper import GameStatus
import pythonsweeper as ps
import pprint as pt
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
# pythonsweeper is a module that contains the game logic written by me
# https://github.com/Shagulka/pysweeper


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="PythonSweeper")

        self.game = ps.Game(10, 10, 20)
        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.grid.attach(self.reset_button, 0, 0, 10, 1)
        
        

        self.buttons = []
        for y in range(10):
            self.buttons.append([])
            for x in range(10):
                button = Gtk.Button()
                button.set_label(" ")
                button.set_size_request(50, 50)
                button.connect("clicked", self.on_button_clicked, x, y)
                self.buttons[y].append(button)
                self.grid.attach(button, x, y, 1, 1)
            

    def on_button_clicked(self, widget, x, y):
        status = self.game.reveal(x, y)
        if status == GameStatus.WIN:
            for y in range(10):
                for x in range(10):
                    self.reveal(x, y)
        self.update_buttons()
        if status == GameStatus.WIN:
            print("You win!")
        elif status == GameStatus.LOSE:
            print("You lose!")
        self.update_buttons()

    def on_reset_button_clicked(self, widget):
        self.game = ps.Game(10, 10, 20)
        self.update_buttons()

    def on_flag_button_clicked(self, widget, x, y):
        self.game.flag(x, y)
        self.update_buttons()

    def update_buttons(self):
        for y in range(10):
            for x in range(10):
                if self.game.player_board[y][x] == 9:
                    self.buttons[y][x].set_label("💣")
                elif self.game.player_board[y][x] == -2:
                    self.buttons[y][x].set_label("🚩")
                elif self.game.player_board[y][x] == -3:
                    self.buttons[y][x].set_label("❓")
                elif self.game.player_board[y][x] == -1:
                    self.buttons[y][x].set_label(" ")
                else:
                    self.buttons[y][x].set_label(
                        str(self.game.player_board[y][x]))
                    


win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
