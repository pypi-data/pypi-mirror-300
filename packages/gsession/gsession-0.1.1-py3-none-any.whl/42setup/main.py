import parsec_setup  # Pour configurer Parsec
import session_setup  # Pour préparer la session (déplacer des dossiers et créer des liens symboliques)
import gnome_favorite_apps_setup  # Pour définir les applications favorites dans GNOME
import launch_chrome_and_vscode  # Pour lancer Chrome et VSCode
import ssh_key_maknager # Pour gérer les clés SSH

def main():
    print("Options disponibles :")
    print("1. Installer Parsec et configurer.")
    print("2. Désinstaller Parsec.")
    print("3. Préparer la session (déplacer et créer des liens symboliques).")
    print("4. Définir les applications favorites dans GNOME.")
    print("5. Lancer Chrome et VSCode.")
    print("6. Gérer les clés SSH.")
    print("7. Autres fonctionnalités à ajouter.")

    choice = input("Choisissez une option : ")

    if choice == "1":
        print("Installation de Parsec en cours...")
        parsec_setup.setup_parsec()
    
    elif choice == "2":
        print("Desinstallation de Parsec en cours...")
        parsec_setup.uninstall_parsec()

    elif choice == "3":
        print("Préparation de la session en cours...")
        session_setup.setup_session()
        print("Préparation de la session terminée.")
    
    elif choice == "4":
        print("Définir les applications favorites dans GNOME...")
        gnome_favorite_apps_setup.set_favorite_apps()
    
    elif choice == "5":
        print("Lancement de Chrome et VSCode...")
        launch_chrome_and_vscode.start()

    elif choice == "6":
        print("Gestion des clés SSH...")
        ssh_key_maknager.manage_ssh()

    elif choice == "7":
        print("Fonctionnalités supplémentaires à ajouter.")

    else:
        print("Option invalide.")

if __name__ == "__main__":
    main()
