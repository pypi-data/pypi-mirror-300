import os
import shutil
import subprocess
import urllib.request

# URL de téléchargement de Parsec
parsec_url = "https://builds.parsec.app/package/parsec-linux.deb"
# Chemins de travail
home_dir = os.path.expanduser("~")
parsec_deb_path = os.path.join(home_dir, "parsec-linux.deb")
parsec_config_dir = os.path.join(home_dir, ".parsec")
desktop_file_path = os.path.join(home_dir, "parsecd.desktop")
local_applications_dir = os.path.join(home_dir, ".local/share/applications")

# Fonction principale pour le setup de Parsec
def setup_parsec():

    # Fonction pour télécharger un fichier depuis une URL
    def download_parsec(url, destination):
        print(f"Téléchargement de Parsec depuis {url}...")
        urllib.request.urlretrieve(url, destination)
        print("Téléchargement terminé.")

    # Fonction pour extraire un .deb avec dpkg
    def extract_deb(deb_path, output_dir):
        print(f"Extraction de {deb_path} vers {output_dir}...")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        subprocess.run(["dpkg-deb", "-x", deb_path, output_dir], check=True)
        print("Extraction terminée.")

    # Fonction pour copier les fichiers du dossier skel
    def copy_skel_to_parsec(skel_dir, parsec_config_dir):
        print(f"Copie du contenu de {skel_dir} vers {parsec_config_dir}...")
        if not os.path.exists(parsec_config_dir):
            os.makedirs(parsec_config_dir)
        if os.path.exists(skel_dir):
            shutil.copytree(skel_dir, parsec_config_dir, dirs_exist_ok=True)
            print("Copie terminée.")
        else:
            print(f"Le dossier {skel_dir} n'existe pas. Vérifiez l'extraction.")

    # Fonction pour modifier le fichier parsec.desktop
    def modify_and_copy_desktop_file(src_desktop_file, dest_desktop_file, user_home):
        if os.path.exists(src_desktop_file):
            print(f"Modification de {src_desktop_file}...")
            with open(src_desktop_file, 'r') as file:
                lines = file.readlines()

            # Modifications des chemins dans le fichier .desktop
            with open(dest_desktop_file, 'w') as file:
                for line in lines:
                    if line.startswith("Exec="):
                        file.write(f"Exec={user_home}/usr/bin/parsecd %u\n")
                    elif line.startswith("Icon="):
                        file.write(f"Icon={user_home}/usr/share/icons/hicolor/256x256/apps/parsecd.png\n")
                    else:
                        file.write(line)

            print(f"Copie du fichier {dest_desktop_file} dans {local_applications_dir}...")
            if not os.path.exists(local_applications_dir):
                os.makedirs(local_applications_dir)
            shutil.copy(dest_desktop_file, local_applications_dir)
            remove_tmp = os.path.join(home_dir, "parsecd.desktop")
            if os.path.exists(remove_tmp):
                os.remove(remove_tmp)
                print(f"Fichier {remove_tmp} supprimé.")
            print("Fichier .desktop modifié et copié.")

            # Rendre le fichier .desktop exécutable avec chmod +x
            dest_desktop_full_path = os.path.join(local_applications_dir, os.path.basename(dest_desktop_file))
            print(f"Application des permissions d'exécution sur {dest_desktop_full_path}...")
            subprocess.run(['chmod', '+x', dest_desktop_full_path], check=True)
            print("Le fichier .desktop est maintenant exécutable.")
        else:
            print(f"Le fichier {src_desktop_file} n'a pas été trouvé.")

    def clean_tmp_files():      
        # Supprimer le fichier .deb téléchargé
        if os.path.exists(parsec_deb_path):
            print(f"Suppression du fichier {parsec_deb_path}...")
            os.remove(parsec_deb_path)
            print("Fichier .deb supprimé.")
        else:
            print(f"{parsec_deb_path} n'existe pas.")

    # Exécution du processus de setup
    try:
        # Téléchargement du paquet Parsec
        download_parsec(parsec_url, parsec_deb_path)
        
        # Extraction du fichier .deb
        extract_deb(parsec_deb_path, home_dir)
        
        # Copie du contenu de skel vers .parsec
        skel_dir = os.path.join(home_dir, "usr/share/parsec/skel")
        copy_skel_to_parsec(skel_dir, parsec_config_dir)
        
        # Modification du fichier .desktop
        desktop_file_src = os.path.join(home_dir, "usr/share/applications/parsecd.desktop")
        modify_and_copy_desktop_file(desktop_file_src, desktop_file_path, home_dir)

        # Nettoyage des fichiers temporaires
        clean_tmp_files()

        subprocess.run(f"{home_dir}/usr/bin/parsecd", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("Configuration terminée avec succès.")
        
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


def uninstall_parsec():
    local_desktop_file = os.path.join(local_applications_dir, "parsecd.desktop")
    local_parsec_file = os.path.join(home_dir, "usr")

    try:
        # Supprimer le répertoire de configuration .parsec
        if os.path.exists(parsec_config_dir):
            print(f"Suppression du répertoire de configuration {parsec_config_dir}...")
            shutil.rmtree(parsec_config_dir)
            print("Répertoire .parsec supprimé.")
        else:
            print(f"{parsec_config_dir} n'existe pas.")

        # Supprimer le répertoire .deb a été extrait
        if os.path.exists(home_dir):
            print(f"Suppression du répertoire d'extraction {local_parsec_file}...")
            shutil.rmtree(local_parsec_file)
            print(f"Répertoire {local_parsec_file} supprimé.")
        else:
            print(f"{local_parsec_file} n'existe pas.")

        # Supprimer le fichier .desktop dans ~/.local/share/applications
        if os.path.exists(local_desktop_file):
            print(f"Suppression du fichier .desktop {local_desktop_file}...")
            os.remove(local_desktop_file)
            print("Fichier .desktop supprimé.")
        else:
            print(f"{local_desktop_file} n'existe pas.")
        
        print("Parsec a été désinstallé avec succès.")
    
    except Exception as e:
        print(f"Une erreur est survenue lors de la désinstallation : {e}")
