from colorama import Fore, Style
import subprocess
import os

# Vérif si la commande 'pip/pip3' est dispo
def check_pip_command():
    try:
        # Vérif si 'pip' est installé
        subprocess.check_output('pip --version', shell=True)
        return 'pip'
    except subprocess.CalledProcessError:
        try:
            # Vérif si 'pip3' est installé
            subprocess.check_output('pip3 --version', shell=True)
            return 'pip3'
        except subprocess.CalledProcessError:
            return None

# Installer 'pip'
def install_pip():
    pip_command = check_pip_command()
    if not pip_command:
        # Installer 'pip' si pas installé
        print(f"{Fore.RED}[!]{Style.RESET_ALL} pip is not installed. Installing...")
        try:
            # Installer 'pip'
            subprocess.check_output('python -m ensurepip --upgrade', shell=True)
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} pip has been installed.")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}[!]{Style.RESET_ALL} Failed to install pip. Please install it manually.")
    else:
        return

# Installer 'requests'
def install_requests():
    pip_command = check_pip_command()
    if pip_command:
        try:
            # Vérif si le module 'requests' est installé
            import requests
            return  # fait rien si 'requests' est installé
        except ImportError:
            # Installer 'requests' si pas installé
            print(f"{Fore.RED}[!]{Style.RESET_ALL} requests is not installed. Installing...")
            try:
                # Installe 'requests' et module SOCKS pour les co proxy
                subprocess.check_output(f'{pip_command} install requests', shell=True)
                subprocess.check_output(f'{pip_command} install requests[socks]', shell=True)
                print(f"{Fore.GREEN}[+]{Style.RESET_ALL} requests has been installed.")
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}[!]{Style.RESET_ALL} Failed to install requests.")
    else:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} pip is not installed, unable to install requests.")

# Installer 'Tor'
def install_tor():
    try:
        # Vérif si Tor est installé
        if os.name == 'nt':
            subprocess.check_output('where tor', shell=True)  # Commande Windows
        else:
            subprocess.check_output('which tor', shell=True)  # Commande Unix/Linux
        return
    except subprocess.CalledProcessError:
        # Affiche un mess si Tor pas installé
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Tor is not installed. Please install Tor manually for your OS.")
        print("Download it from https://www.torproject.org/download/")

# Configurer Tor en fonction de l'OS
def configure_tor():
    if os.name == 'nt':  # Config pour Windows
        user_profile = os.getenv('USERPROFILE')
        tor_directory = os.path.join(user_profile, 'AppData', 'Roaming', 'tor')
    elif os.name == "posix" and "linux" in os.uname().sysname.lower():  # Config pour Linux
        tor_directory = '/etc/tor'
    elif os.name == "posix" and "darwin" in os.uname().sysname.lower():  # Config pour macOS
        tor_directory = '/usr/local/etc/tor'
    else:
        raise NotImplementedError("Unsupported platform")

    # Définition des chemins des files de conf Tor
    torrc_path = os.path.join(tor_directory, 'torrc')
    geoip_path = os.path.join(tor_directory, 'geoip')
    geoipv6_path = os.path.join(tor_directory, 'geoip6')

    # Création du répertoire Tor
    if not os.path.exists(tor_directory):
        os.makedirs(tor_directory)
        print(f" {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Created directory: {tor_directory}")

    # Création du fichier 'torrc'
    if not os.path.exists(torrc_path):
        with open(torrc_path, 'w') as f:
            # Écriture des param de conf dans 'torrc'
            f.write("ControlPort 9051\n")
            f.write("CookieAuthentication 1\n")
            f.write("Log warn stdout\n")
            f.write(f"GeoIPFile {geoip_path}\n")
            f.write(f"GeoIPv6File {geoipv6_path}\n")
        print(f" {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Created torrc file at: {torrc_path}")

    # Création du fichier 'geoip'
    if not os.path.exists(geoip_path):
        open(geoip_path, 'w').close()  # Crée un fichier vide
        print(f" {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Created geoip file at: {geoip_path}")

    # Création du fichier 'geoip6'
    if not os.path.exists(geoipv6_path):
        open(geoipv6_path, 'w').close()  # Crée un fichier vide
        print(f" {Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} Created geoip6 file at: {geoipv6_path}")

if __name__ == "__main__":
    install_pip()
    install_requests()
    install_tor()
    configure_tor()
