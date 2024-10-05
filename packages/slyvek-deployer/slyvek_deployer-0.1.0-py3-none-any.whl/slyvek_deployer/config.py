import os
import json
from getpass import getpass

class ConfigManager:
    CONFIG_FILE = os.path.expanduser("~/.slyvek_config.json")  # Stocké dans le dossier home de l'utilisateur

    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        """Charge la configuration depuis le fichier JSON."""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save_config(self):
        """Sauvegarde la configuration dans le fichier JSON."""
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
        # Définir les permissions du fichier pour qu'il ne soit accessible qu'à l'utilisateur
        os.chmod(self.CONFIG_FILE, 0o600)

    def get(self, key):
        """Récupère la valeur d'une clé de configuration."""
        return self.config.get(key)

    def set(self, key, value):
        """Définit une valeur pour une clé de configuration."""
        self.config[key] = value
        self.save_config()

    def ensure_keys(self, keys):
        """Vérifie que toutes les clés sont présentes, sinon demande à l'utilisateur."""
        missing_keys = [key for key in keys if key not in self.config or not self.config[key]]
        for key in missing_keys:
            prompt_text = f"Entrez {key.replace('_', ' ')} : "
            if 'password' in key or 'api_key' in key:
                value = getpass(prompt_text)
            else:
                value = input(prompt_text)
            self.set(key, value)

    def confirm(self):
        """Affiche la configuration actuelle et demande la confirmation."""
        print("\nConfiguration actuelle :")
        for key, value in self.config.items():
            display_value = value
            print(f"{key.replace('_', ' ')}: {display_value}")

        confirmation = input("\nVoulez-vous continuer avec cette configuration ? (o/N) : ")
        return confirmation.lower() == 'o'

class Config:
    vps_ip = None
    vps_user = None
    vps_password = None
    vps_new_password = None
    api_key = None
    domain = None
    email = None
    github_username = None
    github_password = None
    