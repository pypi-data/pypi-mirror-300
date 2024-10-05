from fabric import Connection
from invoke import task
from .config import Config
import requests

@task
def deploy(c, login_file_path, trious_file_path):
    """Déploie et configure le VPS."""
    vps_ip = Config.vps_ip
    vps_user = Config.vps_user
    vps_password = Config.vps_password

    # Connexion au VPS
    conn = Connection(
        host=vps_ip,
        user=vps_user,
        connect_kwargs={"password": vps_password}
    )

    # Exécuter les tâches sur le VPS
    installer_python(conn)
    creer_venv(conn)
    installer_slyvek_setup(conn)
    configurer_vps(conn)
    start_api(conn)
    upload_file(conn, login_file_path, trious_file_path)
    start_servers(conn)

def installer_python(conn):
    """Installe Python et les dépendances nécessaires sur le VPS."""
    print("Installation de Python et des dépendances...")
    conn.sudo("apt update && apt upgrade -y")
    conn.sudo("apt install -y python3 python3-pip python3-venv git")

def creer_venv(conn):
    """Crée un environnement virtuel sur le VPS."""
    print("Création de l'environnement virtuel...")
    conn.run("python3 -m venv ~/slyvek_env")

def installer_slyvek_setup(conn):
    """Installe le package slyvek-setup dans le venv."""
    print("Installation de slyvek-setup...")
    conn.run("~/slyvek_env/bin/pip install slyvek-setup")

def configurer_vps(conn):
    """Configure le VPS en exécutant le script slyvek_setup."""
    print("Configuration du VPS avec slyvek-setup...")

    api_key = Config.api_key
    domain = Config.domain
    email = Config.email
    github_username = Config.github_username
    github_password = Config.github_password

    # Exécuter slyvek-setup avec les arguments nécessaires
    conn.run(
        f"~/slyvek_env/bin/slyvek-setup "
        f"--api-key '{api_key}' "
        f"--email '{email}' "
        f"--domain '{domain}' "
        f"--username '{github_username}' "
        f"--password '{github_password}'"
    )
    new_password = Config.vps_new_password

    conn.run(f"echo root:{new_password} | sudo chpasswd")

def start_api(conn):
    """Démarre l'API sur le VPS."""
    print("Creation de l'environnement virtuel...")
    conn.run("python3 -m venv ~/SlyvekVps/SlyvekApi/venv")

    print("Installation des dépendances...")
    conn.run("source ~/SlyvekVps/SlyvekApi/venv/bin/activate && pip install -r ~/SlyvekVps/SlyvekApi/requirements.txt")

    print("Démarrage de l'API...")
    conn.run("~/SlyvekVps/Scripts/slyvek.sh -api-start")

def upload_file(conn, login_path, trious_path):
    """Upload a file to the remote server."""
        
    url = "https://backend.slyvek.com/update"

    header = {
        "x-api-key": Config.api_key
    }

    conn.run("mkdir -p ~/Slyvek/Slyvek_LoginServer/login")
    conn.run("mkdir -p ~/Slyvek/Slyvek_GameServers/trious")

    with open(login_path, 'rb') as f:
        files = {
            'file': f
        }

        response = requests.post(url, headers=header, files=files)

        if response.status_code == 200:
            print("Login serveur deployée avec succès.")
        else:
            print("Erreur lors du déploiement du fichier.")
            print(f"Code d'erreur : {response.status_code}")
            print(f"Message d'erreur : {response.text}")

    with open(trious_path, 'rb') as f:
        files = {
            'file': f
        }

        response = requests.post(url, headers=header, files=files)

        if response.status_code == 200:
            print("Trious serveur deployé avec succès.")
        else:
            print("Erreur lors du déploiement du fichier.")
            print(f"Code d'erreur : {response.status_code}")
            print(f"Message d'erreur : {response.text}")
        
def start_servers(conn):
    """Démarre les serveurs sur le VPS."""
    print("Démarrage des serveurs login et trious...")
    conn.run("~/SlyvekVps/Scripts/slyvek.sh -s login slyvek")
    conn.run("~/SlyvekVps/Scripts/slyvek.sh -s trious slyvek")