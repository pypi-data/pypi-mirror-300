import subprocess
import os

def launch_chrome():
    # Chemin de l'exécutable de Google Chrome (assure-toi que c'est le bon chemin)
    chrome_path = '/usr/bin/google-chrome'

    # Vérifier si le chemin de Google Chrome est correct
    if os.path.exists(chrome_path):
        print("Lancement de Google Chrome pour l'authentification...")
        # Lancer Google Chrome et attendre qu'il se ferme
        subprocess.Popen([chrome_path])
        print("Google Chrome fermé. Continuer...")
    else:
        print(f"Google Chrome n'est pas trouvé à {chrome_path}. Vérifiez le chemin.")
        return False
    
    return True

def launch_vscode():
    # Chemin de l'exécutable de VSCode (assure-toi que c'est le bon chemin)
    vscode_path = '/usr/bin/code'

    # Vérifier si le chemin de VSCode est correct
    if os.path.exists(vscode_path):
        print("Lancement de Visual Studio Code pour la synchronisation...")
        # Lancer Visual Studio Code
        subprocess.Popen([vscode_path])
    else:
        print(f"Visual Studio Code n'est pas trouvé à {vscode_path}. Vérifiez le chemin.")

def start():
    # Lancer Google Chrome pour l'authentification
    if launch_chrome():
        # Si Chrome se ferme correctement, lancer VSCode
        launch_vscode()
