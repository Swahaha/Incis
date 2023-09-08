import tkinter as tk
from tkinter import *
import os
import pyautogui
import datetime
import win32clipboard as clip
import win32con
from io import BytesIO
from PIL import ImageGrab, Image
from pytesseract import pytesseract

#hello
print("hello")

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Incis")
        self.master.geometry("300x50")

        self.button_frame = Frame(master)
        self.button_frame.pack()

        self.snipButton = Button(self.button_frame, text="Get snippet", command=self.create_screen_canvas, background="green")
        self.snipButton.pack(side=LEFT, padx=5)

        self.button_clear = Button(self.button_frame, text="Copy Text", command=self.copy_text)
        self.button_clear.pack(side=LEFT, padx=5)
        self.button_clear.pack_forget()

        self.textbox = Text(master, wrap=WORD, height=1)
        self.textbox.pack()
        self.textbox.pack_forget()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)

        self.snip_surface = None
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        self.tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.pytesseract_path = r'C:\Users\Swarajh Mehta\Desktop\Projects\Incisus\trial.jpg'
        pytesseract.tesseract_cmd = self.tesseract_path

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        self.master.withdraw()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.display_rectangle_position()

        x, y, width, height = self.get_screenshot_dimensions()

        self.take_bounded_screenshot(x, y, width, height)

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()

        self.textbox.pack()
        self.button_clear.pack()
        self.textbox.delete('1.0', END)
        copied_text = self.get_clipboard_text()
        self.textbox.insert(END, copied_text)
        self.update_textbox_size()

        self.master_screen.withdraw()
        self.master.deiconify()

    def on_button_press(self, event):
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)

    def get_screenshot_dimensions(self):
        x = min(self.start_x, self.current_x)
        y = min(self.start_y, self.current_y)
        width = abs(self.current_x - self.start_x)
        height = abs(self.current_y - self.start_y)
        return x, y, width, height

    def update_textbox_size(self):
        self.textbox.update_idletasks()
        line_count = int(self.textbox.index(END).split('.')[0])
        char_width = self.get_text_width() + 5
        self.textbox.config(height=line_count, width=char_width)
        self.master.geometry("")

    def get_text_width(self):
        text = self.textbox.get('1.0', END)
        lines = text.split('\n')
        max_length = max(len(line) for line in lines)
        return max_length

    def copy_text(self):
        edited_text = self.textbox.get('1.0', END)
        self.set_clipboard_text(edited_text)

    def take_bounded_screenshot(self, x, y, width, height):
        image = pyautogui.screenshot(region=(x, y, width, height))

        image.save(self.pytesseract_path)

        img = Image.open(self.pytesseract_path)
        data = pytesseract.image_to_string(img, config='-c preserve_interword_spaces=1')

        self.set_clipboard_text(data)

    def set_clipboard_text(self, text):
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardText(text)
        clip.CloseClipboard()

    def get_clipboard_text(self):
        clip.OpenClipboard()
        text = clip.GetClipboardData()
        clip.CloseClipboard()
        return text


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
