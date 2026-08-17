import os
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

from constants import IMAGE_FOLDER

class BingoCallerFullscreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Caller")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # load and shuffle images
        self.images = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) 
                       if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
        random.shuffle(self.images)
        
        self.current_index = -1

        # UI
        self.image_label = tk.Label(root, bg="black")
        self.image_label.pack(expand=True, fill="both")

        # key events
        self.root.bind('<space>', lambda event: self.next_image())
        self.root.bind('<Right>', lambda event: self.next_image())
        self.root.bind('<Left>', lambda event: self.prev_image())
        self.root.bind('<Escape>', lambda event: self.root.destroy())

    def draw_image(self):
        if 0 <= self.current_index < len(self.images):
            img_path = self.images[self.current_index]
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            
            img = Image.open(img_path)
            img = ImageOps.exif_transpose(img)
            img.thumbnail((screen_w, screen_h))
            photo = ImageTk.PhotoImage(img)

            self.image_label.config(image=photo)
            self.image_label.image = photo

    def next_image(self):
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.draw_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.draw_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = BingoCallerFullscreen(root)
    root.mainloop()
