import os
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

from constants import IMAGE_FOLDER, DISPLAY_TIME_MS, DIASHOW_IMAGE_FOLDER

class BingoSlideshow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Diashow")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # load images
        image_folder = DIASHOW_IMAGE_FOLDER if DIASHOW_IMAGE_FOLDER else IMAGE_FOLDER
        self.all_images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) 
                           if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

        self.current_playlist = []
        self.timer_id = None

        # UI
        self.image_label = tk.Label(root, bg="black")
        self.image_label.pack(expand=True, fill="both")

        self.root.bind('<Escape>', lambda event: self.root.destroy())
        if self.all_images:
            self.show_next_image()

    def show_next_image(self):
        # (re)shuffle and add to playlist if empty
        if not self.current_playlist:
            self.current_playlist = self.all_images.copy()
            random.shuffle(self.current_playlist)

        img_path = self.current_playlist.pop()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)
        img.thumbnail((screen_w, screen_h))
        photo = ImageTk.PhotoImage(img)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        # delay before showing next image
        self.timer_id = self.root.after(DISPLAY_TIME_MS, self.show_next_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = BingoSlideshow(root)
    root.mainloop()
