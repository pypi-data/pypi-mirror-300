from invoke import Context
from .fabfile import deploy
from .config import ConfigManager, Config
import tkinter as tk
from tkinter import filedialog

def open_file_dialog(name):
    root = tk.Tk()
    root.withdraw()
    print(f"Ouverture de la boîte de dialogue pour sélectionner un fichier ZIP nommé {name}...")

    # Ouvrir la boîte de dialogue pour sélectionner un fichier .zip
    file_path = filedialog.askopenfilename(
        title=f"Choisissez un fichier ZIP nommé {name}",
        filetypes=[("Fichiers ZIP", "*.zip")]
    )

    # Fermer proprement Tkinter
    root.quit()
    root.destroy()

    if file_path:
        print(f"Fichier sélectionné : {file_path}")
        return file_path
    else:
        print("Aucun fichier sélectionné.")
        return None

def main():
    login_file_path = open_file_dialog("login.zip")
    trious_file_path = open_file_dialog("trious.zip")
    if not login_file_path or not trious_file_path:
        print("Aucun fichier sélectionné, les serveurs login et trious n'ont pas été push.")
        return
    
    config = ConfigManager()

    required_keys = [
        'vps_ip',
        'vps_user',
        'vps_password',
        'vps_new_password',
        'api_key',
        'domain',
        'email',
        'github_username',
        'github_password',
    ]

    config.ensure_keys(required_keys)

    if not config.confirm():
        print("Configuration annulée.")
        return

    Config.vps_ip = config.get('vps_ip')
    Config.vps_user = config.get('vps_user')
    Config.vps_password = config.get('vps_password')
    Config.vps_new_password = config.get('vps_new_password')
    Config.api_key = config.get('api_key')
    Config.domain = config.get('domain')
    Config.email = config.get('email')
    Config.github_username = config.get('github_username')
    Config.github_password = config.get('github_password')



    ctx = Context()

    deploy(ctx, login_file_path, trious_file_path)

if __name__ == "__main__":
    main()
