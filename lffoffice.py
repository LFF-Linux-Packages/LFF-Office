import tkinter as tk
from tkinter import messagebox
import subprocess
import getpass
username = getpass.getuser()
# Main Application
class LFFOfficeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("LFF Office Suite")

        self.logo_image = tk.PhotoImage(file="~/lffoffice.png")  # Replace with the actual path to your logo.png

        self.create_widgets()

        self.window.mainloop()

    def create_widgets(self):
        logo_label = tk.Label(self.window, image=self.logo_image)
        logo_label.pack()

        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack()

        open_lffw_button = tk.Button(buttons_frame, text="Open .lffw", command=self.open_lff_word)
        open_lffw_button.pack(side=tk.LEFT, padx=10)

        open_lffp_button = tk.Button(buttons_frame, text="Open .lffp", command=self.open_lff_presentations)
        open_lffp_button.pack(side=tk.LEFT, padx=10)

        open_lffg_button = tk.Button(buttons_frame, text="Open .lffg", command=self.open_lff_grids)
        open_lffg_button.pack(side=tk.LEFT, padx=10)

    def open_lff_word(self):
        subprocess.Popen(["python3", f"/home/{username}/.local/share/applications/LFF-Office/LFF-Word/lffofficeword.py"])  # Replace with the actual path to lffofficeword.py

    def open_lff_presentations(self):
        subprocess.Popen(["python3", "/path/to/lffofficepresentations.py"])  # Replace with the actual path to lffofficepresentations.py

    def open_lff_grids(self):
        subprocess.Popen(["python3", "/path/to/lffofficegrids.py"])  # Replace with the actual path to lffofficegrids.py

# Run the LFF Office App
app = LFFOfficeApp()