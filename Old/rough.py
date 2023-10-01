import tkinter as tk

class TextBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Textbox Auto-Resize")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.button_insert = tk.Button(self.button_frame, text="Insert Text", command=self.insert_text)
        self.button_insert.pack(side=tk.LEFT, padx=5)

        self.button_clear = tk.Button(self.button_frame, text="Clear Text", command=self.clear_text)
        self.button_clear.pack(side=tk.LEFT, padx=5)
        self.button_clear.pack_forget()  # Initially hide the Clear Text button

        self.textbox = tk.Text(root, wrap=tk.WORD, height=1)
        self.textbox.pack()
        self.textbox.pack_forget()  # Initially hide the textbox

        self.text_to_insert = "This is some example text that will be inserted into the textbox."

    def insert_text(self):
        self.textbox.pack()  # Make the textbox visible
        self.button_clear.pack()  # Make the Clear Text button visible
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert(tk.END, self.text_to_insert)
        self.update_textbox_size()

    def clear_text(self):
        self.textbox.pack_forget()  # Hide the textbox
        self.button_clear.pack_forget()  # Hide the Clear Text button
        self.textbox.delete('1.0', tk.END)
        self.textbox.config(height=1, width=1)

    def update_textbox_size(self):
        self.textbox.update_idletasks()  # Ensure any pending changes are applied immediately
        line_count = int(self.textbox.index(tk.END).split('.')[0])
        char_width = len(self.textbox.get('1.0', tk.END))  # Count the characters in the text
        self.textbox.config(height=line_count, width=char_width)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextBoxApp(root)
    root.mainloop()
