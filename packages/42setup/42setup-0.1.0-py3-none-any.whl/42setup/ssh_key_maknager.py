import os
import subprocess

# Chemin du répertoire SSH de l'utilisateur
ssh_dir = os.path.expanduser("~/.ssh")
private_key_path = os.path.join(ssh_dir, "id_rsa")
public_key_path = os.path.join(ssh_dir, "id_rsa.pub")

def check_ssh_key_exists():
    """Vérifie si la clé SSH existe déjà."""
    return os.path.exists(private_key_path) and os.path.exists(public_key_path)

def create_ssh_key():
    """Crée une nouvelle paire de clés SSH pour l'utilisateur avec ssh-keygen."""
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)
        os.chmod(ssh_dir, 0o700)  # Assurer les bonnes permissions

    print("Création d'une nouvelle clé SSH...")
    # Exécuter la commande ssh-keygen sans paramètres avancés, laissant les valeurs par défaut
    subprocess.run(["ssh-keygen", "-f", private_key_path], check=True)
    print(f"Clé SSH créée : {private_key_path}")

def display_public_key():
    """Affiche la clé publique SSH existante."""
    if os.path.exists(public_key_path):
        with open(public_key_path, "r") as pubkey_file:
            public_key = pubkey_file.read()
            print(f"Clé publique SSH existante :\n{public_key}")
    else:
        print("Aucune clé publique SSH trouvée.")

def manage_ssh():
    if check_ssh_key_exists():
        print("Une clé SSH existe déjà.")
        display_public_key()
    else:
        create_ssh_key()

