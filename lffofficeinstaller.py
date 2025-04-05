import os
import getpass
import shutil

def search_files(directory, extension):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files

# Get the username of the account
username = getpass.getuser()

# Directory to search within
directory_to_search = f'/home/{username}'

# Search for lffofficeword.py files
lffword_python = search_files(directory_to_search, 'lffoffice.py')
lffword_png = search_files(directory_to_search, 'lffoffice.png')

def create_desktop_entry():
    desktop_entry = f'''[Desktop Entry]
Type=Application
Name=LFF Office Hub
Exec=/usr/bin/python3 /home/{username}/.local/share/applications/LFF-Office/lffoffice.py
Terminal=false
Icon=/home/{username}/.local/share/applications/LFF-Office/lffoffice.png
Categories=Office;
'''

    # Specify the path and filename for the desktop entry file
    desktop_entry_file = f'/home/{username}/.local/share/applications/LFF-Office.desktop'
    destination_dir = f'/home/{username}/.local/share/applications/LFF-Office/'

    # Create the necessary directories
    os.makedirs(destination_dir, exist_ok=True)

    # Copy each lffofficeword.py file individually
    for file in lffword_python:
        filename = os.path.basename(file)
        destination = os.path.join(destination_dir, filename)
        shutil.copy2(file, destination)
    for file in lffword_png:
        filename = os.path.basename(file)
        destination = os.path.join(destination_dir, filename)
        shutil.copy2(file, destination)

    with open(desktop_entry_file, 'w') as f:
        f.write(desktop_entry)

    # Set execute permissions on the desktop entry file
    os.chmod(desktop_entry_file, 0o755)

# Run the create_desktop_entry() function to create the desktop entry
create_desktop_entry()
print('LFF Office Hub has been successfully installed!')