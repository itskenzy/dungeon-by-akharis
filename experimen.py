import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import random

class DungeonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Game")
        self.root.geometry("500x700")

        # Petunjuk
        self.hint_label = tk.Label(root, text="Gunakan w, a, s, d untuk bergerak", font=("Arial", 14))
        self.hint_label.pack()

        # Peta Dungeon
        self.map_canvas = tk.Canvas(root, width=500, height=500)
        self.map_canvas.pack()

        # Petunjuk Gerakan
        self.message_label = tk.Label(root, text="", font=("Arial", 14))
        self.message_label.pack()

        # Inisialisasi pemain, monster, petualang, dan pintu keluar
        self.dungeon = Dungeon(5, 5)
        self.player = Player(0, 0)
        self.pintu_keluar = PintuKeluar(4, 4)
        self.monsters = [Monster(4, 3), Monster(3, 4), Monster(3, 1), Monster(2, 3), Monster(1, 1), Monster(2, 4), Monster(2, 2)]
        self.petualang = Petualang(4, 0)

        # Load images
        self.load_images()

        # Render peta awal
        self.update_map()

        # Bind tombol keyboard
        self.root.bind("<Key>", self.handle_keypress)

    def load_images(self):
        self.map_image = ImageTk.PhotoImage(Image.open("texture_map.png").resize((500, 500)))
        self.player_image = ImageTk.PhotoImage(Image.open("texture_knight.png").resize((100, 100)))
        self.monster_image = ImageTk.PhotoImage(Image.open("texture_skull.png").resize((100, 100)))
        self.petualang_image = ImageTk.PhotoImage(Image.open("texture_sword.png").resize((100, 100)))
        self.exit_image = ImageTk.PhotoImage(Image.open("texture_knight.png").resize((100, 100)))

    def handle_keypress(self, event):
        gerakan = event.char
        if gerakan not in ['w', 'a', 's', 'd']:
            self.message_label.config(text="Gerakan tidak valid. Coba lagi.")
            return

        if self.player.gerak(gerakan):
            self.update_map()
            self.check_conditions()
        else:
            self.message_label.config(text="Anda tidak bisa bergerak ke arah tersebut. Coba arah yang lain.")

    def check_conditions(self):
        if (self.player.x, self.player.y) == (self.pintu_keluar.x, self.pintu_keluar.y):
            messagebox.showinfo("Selamat!", "Selamat! Anda menemukan pintu keluar dan berhasil keluar dari dungeon!")
            self.root.quit()
        elif any((self.player.x, self.player.y) == (monster.x, monster.y) for monster in self.monsters):
            self.handle_monster_encounter()
        elif (self.player.x, self.player.y) == (self.petualang.x, self.petualang.y):
            self.handle_petualang_encounter()
        else:
            self.message_label.config(text="Anda bergerak ke langkah berikutnya.")

    def handle_monster_encounter(self):
        self.message_label.config(text="Oh tidak! Anda bertemu dengan monster!")
        if self.ask_math_question():
            self.message_label.config(text="Anda mengalahkan monster!")
            self.monsters = [m for m in self.monsters if (m.x, m.y) != (self.player.x, self.player.y)]
        else:
            messagebox.showinfo("Kalah", "Jawaban salah! Anda kalah!")
            self.root.quit()

    def handle_petualang_encounter(self):
        self.message_label.config(text="Anda bertemu dengan petualang! Bantu melawan monster!")
        if self.ask_math_question():
            self.message_label.config(text="Anda berhasil membantu petualang!")
        else:
            messagebox.showinfo("Kalah", "Jawaban salah! Anda kalah!")
            self.root.quit()

    def ask_math_question(self):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        answer = a + b
        user_answer = simpledialog.askinteger("Kuis Matematika", f"Berapakah {a} + {b}?")
        return user_answer == answer

    def update_map(self):
        self.map_canvas.delete("all")
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)

        # Posisi objek di grid 5x5 dengan ukuran masing-masing 100x100 px
        for monster in self.monsters:
            self.map_canvas.create_image(monster.x * 100, monster.y * 100, anchor=tk.NW, image=self.monster_image)
        self.map_canvas.create_image(self.petualang.x * 100, self.petualang.y * 100, anchor=tk.NW, image=self.petualang_image)
        self.map_canvas.create_image(self.pintu_keluar.x * 100, self.pintu_keluar.y * 100, anchor=tk.NW, image=self.exit_image)
        self.map_canvas.create_image(self.player.x * 100, self.player.y * 100, anchor=tk.NW, image=self.player_image)

class Dungeon:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def gerak(self, arah):
        if arah == 'w' and self.y > 0:
            self.y -= 1
            return True
        elif arah == 's' and self.y < 4:
            self.y += 1
            return True
        elif arah == 'a' and self.x > 0:
            self.x -= 1
            return True
        elif arah == 'd' and self.x < 4:
            self.x += 1
            return True
        else:
            return False

class PintuKeluar:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Petualang:
    def __init__(self, x, y):
        self.x = x
        self.y = y

if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonApp(root)
    root.mainloop()
