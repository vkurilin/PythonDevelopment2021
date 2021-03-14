import itertools
import tkinter as tk
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Optional

from sympy.combinatorics.permutations import Permutation


class GameData:
    Position = namedtuple('Position', ['row', 'column'])
    PermutationType = list[Optional[int]]

    rows: int
    columns: int
    permutation: PermutationType = []
    empty_cell_index: int = 0

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.shuffle()

    @property
    def total_number_of_cells(self) -> int:
        return self.rows * self.columns

    def shuffle(self) -> PermutationType:
        while permutation := Permutation.random(self.total_number_of_cells - 1):
            if permutation.is_odd:
                break

        self.permutation = list(map(lambda x: x + 1, permutation))
        self.permutation.append(None)
        self.empty_cell_index = 15
        return self.permutation

    def make_move(self, position: Position) -> Position:
        row, column = position
        index = row * self.columns + column

        empty_cell_position = GameData.Position(*divmod(self.empty_cell_index, self.columns))
        kek = abs(empty_cell_position.row - row) + abs(empty_cell_position.column - column)
        if abs(empty_cell_position.row - row) + abs(empty_cell_position.column - column) != 1:
            return position

        self.permutation[index], self.permutation[self.empty_cell_index] = \
            self.permutation[self.empty_cell_index], self.permutation[index]

        self.empty_cell_index = index

        return empty_cell_position

    def check_if_game_won(self):
        return self.permutation == list(range(1, self.total_number_of_cells + 1)) + [None]


game_data = GameData(4, 4)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.buttons = {}
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        for i in range(game_data.rows + 1):
            self.grid_rowconfigure(i, weight=1, uniform='row')
        for i in range(game_data.columns):
            self.grid_columnconfigure(i, weight=1, uniform='col')

        for i in range(1, game_data.total_number_of_cells):
            button = tk.Button(self, text=str(i))
            self.buttons[i] = button

        self.shuffle()

        new = tk.Button(self, text='New', command=self.shuffle)
        quit = tk.Button(self, text='Exit', command=exit)
        new.grid(row=game_data.rows, column=0)
        quit.grid(row=game_data.rows, column=1)

    def make_move(self, button, position):
        print(f'Clicked {position}')
        new_row, new_column = game_data.make_move(position)
        button.grid(
            row=new_row,
            column=new_column,
            sticky=tk.N + tk.E + tk.S + tk.W
        )
        button['command'] = lambda button=button, position=GameData.Position(new_row, new_column): \
            self.make_move(button, position)

    def shuffle(self):
        game_data.shuffle()

        for value, (row, column) in \
                zip(game_data.permutation, itertools.product(range(game_data.rows), range(game_data.columns))):
            if value is None:
                continue
            button = self.buttons.get(value)
            button['command'] = lambda button=button, position=GameData.Position(row, column): \
                self.make_move(button, position)
            button.grid(row=row, column=column, sticky=tk.N + tk.E + tk.S + tk.W)

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
