import customtkinter as ctk
from PIL import Image
import random

GRID_SIZE = 5
NUM_MINES = 5

class Cell(ctk.CTkButton):
    def __init__(self, master, x, y, is_mine, bomb_image):
        super().__init__(
            master,
            width=50,
            height=50,
            corner_radius=6,
            text="",
            font=("Segoe UI", 16),
            fg_color="#2e2e2e",
            command=self.reveal
        )
        self.master = master
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.revealed = False
        self.bomb_image = bomb_image
        self.grid(row=y, column=x, padx=3, pady=3)

    def reveal(self):
        if self.revealed:
            return
        self.revealed = True

        if self.is_mine:
            self.configure(image=self.bomb_image, text="", fg_color="#8b0000")
            self.master.reveal_all_mines()
        else:
            count = self.master.count_adjacent_mines(self.x, self.y)
            self.configure(text=str(count) if count > 0 else "", fg_color="#444444")

            if count == 0:
                self.master.reveal_adjacent(self.x, self.y)

class Minesweeper(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Сапёр")
        ctk.set_appearance_mode("dark")
        self.geometry(f"{GRID_SIZE * 60}x{GRID_SIZE * 60}")
        self.resizable(False, False)

        try:
            self.iconbitmap("bomb.ico")
        except Exception as e:
            print("⚠️ Не удалось установить иконку окна:", e)

        bomb_pil = Image.open("bomb.png")
        self.bomb_image = ctk.CTkImage(light_image=bomb_pil, size=(32, 32))

        self.cells = []
        self.create_grid()

    def create_grid(self):
        mine_positions = random.sample(range(GRID_SIZE * GRID_SIZE), NUM_MINES)
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                index = y * GRID_SIZE + x
                is_mine = index in mine_positions
                cell = Cell(self, x, y, is_mine, self.bomb_image)
                row.append(cell)
            self.cells.append(row)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if self.cells[ny][nx].is_mine:
                        count += 1
        return count

    def reveal_adjacent(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    self.cells[ny][nx].reveal()

    def reveal_all_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.revealed:
                    cell.configure(image=self.bomb_image, text="", fg_color="#8b0000")
                    cell.revealed = True

if __name__ == "__main__":
    app = Minesweeper()
    app.mainloop()

