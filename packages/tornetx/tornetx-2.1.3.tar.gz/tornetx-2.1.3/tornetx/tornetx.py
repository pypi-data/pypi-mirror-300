from tornetx.utils import install_pip, install_requests, install_tor, configure_tor
from tornetx.banner import print_banner
from colorama import init, Fore, Style
from stem.control import Controller
from sys import platform
from stem import Signal
import subprocess
import argparse
import requests
import signal
import time
import os

# Initialisation des couleurs
init(autoreset=True)

# Nom de l'outil
TOOL_NAME = "tornetx"

# Vérif si Tor est installé
def is_tor_installed():
    try:
        # Commande pour vérif l'installation de Tor sous Win
        if platform == "win32":
            subprocess.check_output('where tor', shell=True)
        else:
            # Commande pour Linux
            subprocess.check_output('which tor', shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

# installations (pip, requests, Tor, etc.)
def initialize_environment():
    install_pip()
    install_requests()
    install_tor()
    configure_tor()
    try:
        # Démarrage de Tor selon plateforme (Windows/Linux)
        if platform == "win32":
            subprocess.Popen(['tor'], shell=True)
        else:
            subprocess.Popen(['tor'], shell=False)
        print_start_message()
    except Exception as e:
        print(f"Failed to start Tor: {e}")

# Print un mess une fois que Tor a démarré
def print_start_message():
    print(f"{Fore.WHITE} [{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Tor service started. Please wait a minute for Tor to connect.")
    print(f"{Fore.WHITE} [{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Make sure to configure your browser to use Tor for anonymity.")

# Récup de l'IP en utilisant Tor si dispo, sinon IP normale
def ma_ip():
    if is_tor_running():
        return ma_ip_tor()
    else:
        return ma_ip_normal()

# Vérif si Tor est en cours
def is_tor_running():
    try:
        # Commande pour vérif Tor sous Windows
        if platform == "win32":
            subprocess.check_output('tasklist | findstr /I tor.exe', shell=True)
        else:
            # Commande pour Linux
            subprocess.check_output('pgrep -x tor', shell=False)
        return True
    except subprocess.CalledProcessError:
        return False

# Récup de l'IP via le réseau Tor
def ma_ip_tor():
    url = 'https://api.ipify.org'
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    try:
        # Requête pour obtenir l'IP à travers le proxy Tor
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        print(f'{Fore.WHITE} [{Fore.RED}!{Fore.WHITE}] {Fore.RED}Having trouble connecting to the Tor network. Wait a minute.{Style.RESET_ALL}')
        return None

# Récup de l'IP en utilisant la connexion normale
def ma_ip_normal():
    try:
        # Requête simple pour obtenir l'IP
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        print(f'{Fore.WHITE} [{Fore.RED}!{Fore.WHITE}] {Fore.RED}Having trouble fetching the IP address. Please check your internet connection.{Style.RESET_ALL}')
        return None

# Changement de l'IP via Tor
def change_ip():
    try:
        # Envoi du signal NEWNYM pour forcer le changement d'IP via Tor
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            new_ip = ma_ip_tor()
            if new_ip:
                print(f"{Fore.GREEN}Tor IP changed successfully: {new_ip}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Failed to retrieve new Tor IP.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to change Tor IP: {e}{Style.RESET_ALL}")

# Changement répété de l'IP à un intervalle défini
def change_ip_repeatedly(interval, count):
    if count == 0:
        while True:
            # Pause entre les changements d'IP
            time.sleep(interval)
            new_ip = change_ip()
            if new_ip:
                print_ip(new_ip)
    else:
        # Boucle pour changer l'IP un certain nombre de fois
        for _ in range(count):
            time.sleep(interval)
            new_ip = change_ip()
            if new_ip:
                print_ip(new_ip)

# Affichage de l'IP
def print_ip(ip):
    print(f'{Fore.WHITE} [{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Your IP has been changed to {Fore.WHITE}:{Fore.GREEN} {ip}')

# Réinstallation et mise à jour des paquets
def auto_fix():
    install_pip()
    install_requests()
    install_tor()
    subprocess.check_output('pip install --upgrade tornetx', shell=True)

# Arrêt des services Tor
def stop_services():
    try:
        if platform == "win32":
            subprocess.check_output('tasklist | findstr /I tor.exe', shell=True)
            subprocess.check_output("taskkill /IM tor.exe /F", shell=True)
        else:
            subprocess.check_output("pkill -f tor", shell=False)
        print(f"{Fore.WHITE} [{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Tor services and {TOOL_NAME} processes stopped.{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        pass

# Gestion pour arrêter les services si l'user ferme le prog
def signal_handler(sig, frame):
    stop_services()
    print(f"\n{Fore.WHITE} [{Fore.RED}!{Fore.WHITE}] {Fore.RED}Program terminated by user.{Style.RESET_ALL}")
    exit(0)

# Vérif continue de la co internet
def check_internet_connection():
    while True:
        time.sleep(1)
        try:
            # Tentative de requête pour s'assurer que la co est toujours actif
            requests.get('http://www.google.com', timeout=1)
        except requests.RequestException:
            print(f"{Fore.WHITE} [{Fore.RED}!{Fore.WHITE}] {Fore.RED}Internet connection lost. Please check your internet connection.{Style.RESET_ALL}")
            return False

def main():
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)

    # Gestion des arguments argparse
    parser = argparse.ArgumentParser(description="TorNetX - Automate IP address changes using Tor")
    parser.add_argument('--interval', type=int, default=60, help='Time in seconds between IP changes (minimum: 10 seconds)')
    parser.add_argument('--count', type=int, default=10, help='Number of times to change the IP. If 0, change IP indefinitely')
    parser.add_argument('--ip', action='store_true', help='Display the current IP address and exit')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix issues (install/upgrade packages)')
    parser.add_argument('--stop', action='store_true', help='Stop all Tor services and tornetx processes and exit')
    parser.add_argument('--version', action='version', version='%(prog)s 2.1.3')
    args = parser.parse_args()

    # Vérif des valeurs min pour pas surcharger le réseau
    if args.interval < 10:
        print(f"\n [{Fore.RED}!{Fore.WHITE}] {Fore.RED}Minimum interval is 10 seconds to avoid overloading the network. Exiting.{Style.RESET_ALL}")
        return

    # Affichage de l'IP actuelle
    if args.ip:
        ip = ma_ip()
        if ip:
            print_ip(ip)
        return

    # Vérif si Tor est installé
    if not is_tor_installed():
        print(f"{Fore.WHITE} [{Fore.RED}!{Fore.WHITE}] {Fore.RED}Tor is not installed. Please install Tor and try again.{Style.RESET_ALL}")
        return

    # Auto-fix des services si demandé
    if args.auto_fix:
        auto_fix()
        print(f"{Fore.WHITE} [{Fore.GREEN}+{Fore.WHITE}] {Fore.GREEN}Auto-fix complete.{Style.RESET_ALL}")
        return

    # Arrêt des services si demandé
    if args.stop:
        stop_services()
        return

    # Démarrage du prog
    print_banner()
    initialize_environment()
    change_ip_repeatedly(args.interval, args.count)

# Démarrage du script en tant que prog principal
if __name__ == "__main__":
    check_internet_connection()
    main()
