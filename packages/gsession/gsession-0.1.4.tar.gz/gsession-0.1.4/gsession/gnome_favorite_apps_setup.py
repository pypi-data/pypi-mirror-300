import subprocess

def set_favorite_apps():
    # Définir les applications favorites pour GNOME
    favorite_apps = [
        'parsecd.desktop',
        'org.gnome.Nautilus.desktop',
        'org.gnome.Terminal.desktop',
        'google-chrome.desktop',
        'code.desktop',
        'ftpkg.desktop'
    ]

    # Commande gsettings pour définir les apps favorites
    command = [
        'gsettings', 'set', 'org.gnome.shell', 'favorite-apps',
        str(favorite_apps)
    ]

    try:
        # Exécution de la commande
        subprocess.run(command, check=True)
        print("Les applications ont été ajoutées aux favoris avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue : {e}")

