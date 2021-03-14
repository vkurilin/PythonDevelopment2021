import tkinter as tk
from dataclasses import dataclass
import random
from sympy.combinatorics.permutations import Permutation


@dataclass
class GameData:
    rows: int
    columns: int
    permutation: list[int]

    def check_parity_of_permutation(self) -> bool:
        return True

game_data = GameData(4, 4, [])


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        for i in range(game_data.rows + 1):
            self.grid_rowconfigure(i, weight=1, uniform='row')
        for i in range(game_data.columns):
            self.grid_columnconfigure(i, weight=1, uniform='col')

        for row in range(game_data.rows):
            for column in range(game_data.columns):
                button = tk.Button(self, text=str(row)+str(column))
                button['command'] = lambda button=button, row=row, column=column: print(f'Hey, {row, column}')
                button.grid(row=row, column=column, sticky=tk.N + tk.E + tk.S + tk.W)

        new = tk.Button(self, text='New', command=lambda: print('New'))
        quit = tk.Button(self, text='Exit', command=exit)
        new.grid(row=game_data.rows, column=0)
        quit.grid(row=game_data.rows, column=1)

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
