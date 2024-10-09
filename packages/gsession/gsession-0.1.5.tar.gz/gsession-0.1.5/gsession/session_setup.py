import os
import shutil

# Chemins vers les répertoires à déplacer et où les placer
goinfre_dir = '/goinfre/glamazer'
vscode_src = os.path.expanduser('~/.vscode')
vscode_dest = os.path.join(goinfre_dir, 'vscode')

chrome_src = os.path.expanduser('~/.config/google-chrome')
chrome_dest = os.path.join(goinfre_dir, 'google-chrome')

code_src = os.path.expanduser('~/.config/Code')
code_dest = os.path.join(goinfre_dir, 'Code')

# Fonction pour déplacer et créer des liens symboliques
def move_and_link(src, dest):
    if os.path.exists(src):
        # Déplacer le dossier
        print(f"Déplacement de {src} vers {dest}...")
        if os.path.exists(dest):
            print(f"Le dossier {dest} existe déjà.")
        else:
            shutil.move(src, dest)
            print(f"Dossier déplacé : {src} -> {dest}")

        # Créer le lien symbolique
        if not os.path.exists(src):
            print(f"Création du lien symbolique de {dest} vers {src}...")
            os.symlink(dest, src)
            print(f"Lien symbolique créé : {src} -> {dest}")
        else:
            print(f"Le lien symbolique {src} existe déjà.")
    else:
        print(f"Le dossier {src} n'existe pas. Aucune action nécessaire.")

# Fonction pour supprimer les liens symboliques et supprimer les dossiers
def remove_last_session():
    if os.path.exists(vscode_dest):
        print(f"Suppression du lien symbolique {vscode_src}...")
        os.remove(vscode_src)
        print(f"Suppression du dossier {vscode_dest}...")
        shutil.rmtree(vscode_dest)
    else:
        print(f"Le lien symbolique {vscode_src} n'existe pas.")

    if os.path.exists(chrome_dest):
        print(f"Suppression du lien symbolique {chrome_src}...")
        os.remove(chrome_src)
        print(f"Suppression du dossier {chrome_dest}...")
        shutil.rmtree(chrome_dest)
    else:
        print(f"Le lien symbolique {chrome_src} n'existe pas.")

    if os.path.exists(code_dest):
        print(f"Suppression du lien symbolique {code_src}...")
        os.remove(code_src)
        print(f"Suppression du dossier {code_dest}...")
        shutil.rmtree(code_dest)
    else:
        print(f"Le lien symbolique {code_src} n'existe pas.")


def setup_session():
    remove_last_session()
    move_and_link(vscode_src, vscode_dest)
    move_and_link(chrome_src, chrome_dest)
    move_and_link(code_src, code_dest)