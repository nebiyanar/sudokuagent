import tkinter as tk
from tkinter import ttk, messagebox
import copy

from backend import generate_sudoku, solve_sudoku, solve_sudoku_steps


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Step Solver")
        self.root.geometry("560x670")
        self.root.resizable(False, False)

        self.entries = []
        self.current_grid = None
        self.solver_generator = None

        self.create_top_bar()
        self.create_board()

    def create_top_bar(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=15)

        tk.Label(top_frame, text="Difficulty:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.difficulty_var = tk.StringVar(value="medium")
        difficulty_box = ttk.Combobox(
            top_frame,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=10
        )
        difficulty_box.pack(side=tk.LEFT, padx=5)

        tk.Button(top_frame, text="Generate", width=9, command=self.generate_game).pack(side=tk.LEFT, padx=4)
        tk.Button(top_frame, text="Solve Step", width=9, command=self.start_step_solver).pack(side=tk.LEFT, padx=4)
        tk.Button(top_frame, text="Next", width=9, command=self.next_step).pack(side=tk.LEFT, padx=4)
        tk.Button(top_frame, text="Solve Immediately", width=16, command=self.solve_immediately).pack(side=tk.LEFT, padx=4)

    def create_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)

        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(
                    board_frame,
                    width=2,
                    font=("Arial", 20),
                    justify="center"
                )

                padx = (4 if j % 3 == 0 else 1, 4 if j % 3 == 2 else 1)
                pady = (4 if i % 3 == 0 else 1, 4 if i % 3 == 2 else 1)

                entry.grid(row=i, column=j, padx=padx, pady=pady, ipady=8)
                row_entries.append(entry)

            self.entries.append(row_entries)

    def load_grid_to_gui(self, grid):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal")
                entry.delete(0, tk.END)

                if grid[i][j] != -1:
                    entry.insert(0, str(grid[i][j]))
                    entry.config(
                        state="disabled",
                        disabledforeground="black",
                        font=("Arial", 20, "bold"),   # 🔥 kalın
                        bg="#e0e0e0"                  # 🔥 gri arka plan
                    )
                else:
                    entry.config(
                        state="normal",
                        font=("Arial", 20),
                        bg="white"
                    )

    def read_grid_from_gui(self):
        grid = []

        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get().strip()

                if value == "":
                    row.append(-1)
                else:
                    if not value.isdigit():
                        raise ValueError(f"Sadece sayı girilebilir. Hatalı değer: {value}")

                    num = int(value)
                    if num < 1 or num > 9:
                        raise ValueError("Sadece 1 ile 9 arasında değer girilebilir.")

                    row.append(num)

            grid.append(row)

        return grid

    def generate_game(self):
        difficulty = self.difficulty_var.get()
        self.current_grid = generate_sudoku(difficulty)
        self.load_grid_to_gui(self.current_grid)
        self.solver_generator = None

    def start_step_solver(self):
        try:
            self.current_grid = self.read_grid_from_gui()
            self.solver_generator = solve_sudoku_steps(self.current_grid)
            messagebox.showinfo("Info", "Adım adım çözüm başladı. İlerlemek için Next'e bas.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def next_step(self):
        if self.solver_generator is None:
            messagebox.showwarning("Warning", "Önce Solve Step butonuna bas.")
            return

        try:
            action, r, c, value = next(self.solver_generator)

            if action == "place":
                self.entries[r][c].config(state="normal", bg="#ccffcc")
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, str(value))

            elif action == "remove":
                self.entries[r][c].config(state="normal", bg="#ffcccc")
                self.entries[r][c].delete(0, tk.END)

            elif action == "done":
                self.reset_entry_colors()
                messagebox.showinfo("Info", "Sudoku çözüldü.")
                self.solver_generator = None

        except StopIteration:
            self.reset_entry_colors()
            messagebox.showinfo("Info", "Çözüm tamamlandı.")
            self.solver_generator = None
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def solve_immediately(self):
        try:
            self.solver_generator = None  # 🔥 KRİTİK

            grid = self.read_grid_from_gui()
            solved_grid = copy.deepcopy(grid)

            if solve_sudoku(solved_grid):
                self.show_solved_grid(solved_grid)
                messagebox.showinfo("Info", "Sudoku hemen çözüldü.")
            else:
                messagebox.showerror("Error", "Bu sudoku çözülemedi.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_solved_grid(self, grid):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal", bg="white")
                entry.delete(0, tk.END)
                entry.insert(0, str(grid[i][j]))
                entry.config(state="disabled")

    def reset_entry_colors(self):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]

                # sadece editable olanları değiştir
                if entry["state"] == "normal":
                    entry.config(bg="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()