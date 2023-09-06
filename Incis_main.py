from tkinter import *
import os
import pyautogui
import datetime

import win32clipboard as clip
import win32con
from io import BytesIO
from PIL import ImageGrab

from PIL import Image
from pytesseract import pytesseract

tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.tesseract_cmd = tesseract_path

def take_bounded_screenshot(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))

    #ML part
    image.save(r'C:\Users\Swarajh Mehta\Desktop\Projects\Incisus\trial.jpg')

    file_name = datetime.datetime.now().strftime("%f")
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')


    #data = output.getvalue()[14:]
    #ML part
    img = Image.open(r'C:\Users\Swarajh Mehta\Desktop\Projects\Incisus\trial.jpg')
    data = pytesseract.image_to_string(img, config='-c preserve_interword_spaces=1', lang = 'hin')

    output.close()
    clip.OpenClipboard()
    clip.EmptyClipboard()
    #clip.SetClipboardData(win32con.CF_DIB, data)
    clip.SetClipboardText(data)
    clip.CloseClipboard()

class Application():
    def __init__(self, master):
        self.snip_surface = None
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        #root.geometry('400x50+200+200')  # set new geometry
        root.geometry('300x50')
        root.title('Incis')

        self.button_frame = Frame(root)
        self.button_frame.pack()

        self.snipButton = Button(self.button_frame, text="Get snippet", command=self.create_screen_canvas, background="green")
        self.snipButton.pack(side=LEFT, padx=5)

        self.button_clear = Button(self.button_frame, text="Copy Text", command=self.copy_text)
        self.button_clear.pack(side=LEFT, padx=5)
        self.button_clear.pack_forget()

        self.textbox = Text(root, wrap=WORD, height=1)
        self.textbox.pack()
        self.textbox.pack_forget()



        #self.menu_frame = Frame(master)
        #self.menu_frame.pack(fill=BOTH, expand=YES, padx=1, pady=1)

        #self.buttonBar = Frame(self.menu_frame, bg="")
        #self.buttonBar.pack()

        #self.snipButton = Button(self.buttonBar, width=5, height=1, command=self.create_screen_canvas, background="green")
        #self.snipButton.pack()

        #ML part
        #self.textBox = Text(height=10, width=100)
        #self.textBox.pack()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

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

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            print("right down")
            take_bounded_screenshot(self.start_x, self.start_y, self.current_x - self.start_x, self.current_y - self.start_y)

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            print("left down")
            take_bounded_screenshot(self.current_x, self.start_y, self.start_x - self.current_x, self.current_y - self.start_y)

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            print("right up")
            take_bounded_screenshot(self.start_x, self.current_y, self.current_x - self.start_x, self.start_y - self.current_y)

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            print("left up")
            take_bounded_screenshot(self.current_x, self.current_y, self.start_x - self.current_x, self.start_y - self.current_y)

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()

        self.textbox.pack()  # Make the textbox visible
        self.button_clear.pack()
        self.textbox.delete('1.0', END)
        clip.OpenClipboard()
        str = clip.GetClipboardData()
        clip.CloseClipboard()
        self.textbox.insert(END, str)
        self.update_textbox_size()

        #ML part
        #clip.OpenClipboard()
        #str = clip.GetClipboardData()
        #clip.CloseClipboard()
        #self.textBox.insert("end", str)

        self.master_screen.withdraw()
        root.deiconify()


    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def display_rectangle_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.current_x)
        print(self.current_y)

    def update_textbox_size(self):
        self.textbox.update_idletasks()  # Ensure any pending changes are applied immediately
        line_count = int(self.textbox.index(END).split('.')[0])
        char_width = self.get_text_width() + 5  # Count the characters in the text
        self.textbox.config(height=line_count, width=char_width)
        root.geometry("")
        #root.geometry(f"{char_width * 8}x400")

    def get_text_width(self):
        text = self.textbox.get('1.0', END)
        lines = text.split('\n')
        max = 20
        for line in lines:
            if len(line) > max:
                max = len(line)
        return max
    
    def copy_text(self):
        clip.OpenClipboard()
        edited = self.textbox.get('1.0', END)
        clip.EmptyClipboard()
        clip.SetClipboardText(edited)
        clip.CloseClipboard()

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
