import tkinter as tk
from tkinter import filedialog, messagebox
import platform
import threading
import os
import time

current_file = None
unsaved_changes = False
file_check_interval = 0.1  # The interval (in seconds) to check for file differences

def open_file():
    global current_file, unsaved_changes

    if unsaved_changes:
        save_prompt = messagebox.askyesnocancel("Save Changes", "Do you want to save changes to the current document?")
        if save_prompt:
            save_file()
        elif save_prompt is None:
            return

    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("LFFW Files", "*.lffw")])
    if filepath:
        with open(filepath, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())
            current_file = filepath
            unsaved_changes = False
            update_header()

def save_file():
    global current_file, unsaved_changes

    if current_file:
        filepath = current_file
    else:
        filepath = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt"), ("LFFW Files", "*.lffw")])
    
    if filepath:
        with open(filepath, 'w') as file:
            file.write(text.get('1.0', tk.END))
            current_file = filepath
            unsaved_changes = False
            update_header()

def new_file():
    global current_file, unsaved_changes

    if unsaved_changes:
        save_prompt = messagebox.askyesnocancel("Save Changes", "Do you want to save changes to the current document?")
        if save_prompt:
            save_file()
        elif save_prompt is None:
            return

    text.delete('1.0', tk.END)
    current_file = None
    unsaved_changes = False
    update_header()

def set_align_left():
    text.tag_configure("alignment", justify='left')
    text.tag_add("alignment", "1.0", "end")

def set_align_center():
    text.tag_configure("alignment", justify='center')
    text.tag_add("alignment", "1.0", "end")

def set_align_right():
    text.tag_configure("alignment", justify='right')
    text.tag_add("alignment", "1.0", "end")

def set_font_size(size):
    text.configure(font=("Arial", size))

def print_content():
    printer_dialog = tk.Toplevel(window)
    printer_dialog.title("Print")

    printer_label = tk.Label(printer_dialog, text="Printer:")
    printer_label.pack(side=tk.LEFT)

    printer_var = tk.StringVar()
    printer_options = get_printer_by_name()  # Retrieve printer names

    printer_var.set(printer_options[0])  # Set the initial value to the first printer option

    printer_dropdown = tk.OptionMenu(printer_dialog, printer_var, *printer_options)
    printer_dropdown.pack(side=tk.LEFT)

    def print_document():
        selected_printer = printer_var.get()
        print_data = text.get("1.0", tk.END)

        # Print document using the selected printer
        if platform.system() == 'Windows':
            import win32print
            printer_name = get_printer_by_name(selected_printer)  # Retrieve printer by name
            if printer_name:
                win32print.SetDefaultPrinter(printer_name)
                win32print.StartDocPrinter(printer_name, 1, ("Document", None, "RAW"))
                win32print.WritePrinter(printer_name, print_data.encode())
                win32print.EndDocPrinter(printer_name)
                messagebox.showinfo("Print", "Printing complete.")
            else:
                messagebox.showerror("Print", "Failed to find the selected printer.")
        elif platform.system() == 'Linux':
            import cups
            printer_name = get_printer_by_name(selected_printer)  # Retrieve printer by name
            if printer_name:
                conn = cups.Connection()
                print_data = print_data.encode()
                conn.printFile(printer_name, "-", "Print Document", {}, print_data)
                messagebox.showinfo("Print", "Printing complete.")
            else:
                messagebox.showerror("Print", "Failed to find the selected printer.")

    print_button = tk.Button(printer_dialog, text="Print", command=print_document)
    print_button.pack()

def get_printer_by_name(printer_name):
    if platform.system() == 'Windows':
        import win32print
        printers = win32print.EnumPrinters(2)  # Retrieves list of printers
        for printer in printers:
            if printer[2] == printer_name:  # Printer name is at index 2 in the tuple
                return printer[1]  # Printer details are at index 1 in the tuple
    elif platform.system() == 'Linux':
        import cups
        conn = cups.Connection()
        printers = conn.getPrinters()
        for printer in printers:
            if printer == printer_name:
                return printer

    return None

def exit_application():
    global unsaved_changes

    if unsaved_changes:
        save_prompt = messagebox.askyesnocancel("Save Changes", "Do you want to save changes to the current document?")
        if save_prompt:
            save_file()
        elif save_prompt is None:
            return

    window.quit()

def on_text_change(event):
    global unsaved_changes
    unsaved_changes = True
    update_header()

def check_file_changes():
    global current_file, unsaved_changes

    while True:
        if current_file:
            try:
                with open(current_file, 'r') as file:
                    file_content = file.read()
                    text_content = text.get('1.0', tk.END).strip()

                    if file_content != text_content:
                        unsaved_changes = True
                    else:
                        unsaved_changes = False
                        update_header()
            except FileNotFoundError:
                unsaved_changes = True

        else:
            unsaved_changes = False
            update_header()

        # Wait for the specified interval before checking again
        time.sleep(file_check_interval)

def update_header():
    if current_file:
        filename = os.path.basename(current_file)
        if unsaved_changes:
            window.title(f"LFF Office Word - {filename} *")
        else:
            window.title(f"LFF Office Word - {filename}")
    else:
        window.title("LFF Office Word")

window = tk.Tk()
window.title("LFF Office Word")

# Top bar
top_bar = tk.Frame(window)
top_bar.pack(side=tk.TOP, fill=tk.X)

menubar = tk.Menu(window)
window.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

#format_menu = tk.Menu(menubar, tearoff=0)
#format_menu.add_command(label="Align Left", #command=set_align_left)
#format_menu.add_command(label="Align Center", #command=set_align_center)
#format_menu.add_command(label="Align Right", #command=set_align_right)

menubar.add_cascade(label="File", menu=file_menu)
#menubar.add_cascade(label="Format", menu=format_menu)

exit_menu = tk.Menu(menubar, tearoff=0)
exit_menu.add_command(label="Exit", command=exit_application)

menubar.add_cascade(label="Options", menu=exit_menu)

text = tk.Text(font=("Arial", 12))
text.pack(fill=tk.BOTH, expand=True)
text.bind("<<Modified>>", on_text_change)
text.pack_propagate(0)
text.grid_propagate(0)

# Create a thread for checking file changes
file_check_thread = threading.Thread(target=check_file_changes)
file_check_thread.daemon = True
file_check_thread.start()

window.mainloop()
