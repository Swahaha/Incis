import tkinter as tk
from tkinter import filedialog
from PIL import Image

class ImageSizeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Size Viewer")

        self.button_load = tk.Button(root, text="Load Image", command=self.load_image)
        self.button_load.pack()

        self.button_resize = tk.Button(root, text="Resize", command=self.resize_image)
        self.button_resize.pack()

        self.textbox = tk.Text(root, height=10, width=30)
        self.textbox.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image_dimensions()

    def display_image_dimensions(self):
        width = self.image.width
        height = self.image.height
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert(tk.END, f"Width: {width}\nHeight: {height}")

    def resize_image(self):
        if hasattr(self, 'image'):
            width = self.image.width
            height = self.image.height
            font_size = self.textbox.tk.call(self.textbox._w, "font", "configure", "-size")
            char_width = font_size[0] / 2  # estimated character width based on font size
            char_height = font_size[1] / 6  # estimated character height based on font size
            self.textbox.config(height=int(height / char_height), width=int(width / char_width))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSizeApp(root)
    root.mainloop()
