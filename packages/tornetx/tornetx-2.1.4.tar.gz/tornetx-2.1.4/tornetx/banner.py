from colorama import init, Fore, Style

# Initialiser colorama pour Windows et Linux
init(autoreset=True)

# Bannière
def print_banner():
    banner = f"""
{Fore.WHITE} +---------------------------------------------------------------+
{Fore.WHITE} |{Fore.GREEN} ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗██╗  ██╗{Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN} ╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝╚██╗██╔╝{Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║    ╚███╔╝ {Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║    ██╔██╗ {Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   ██╔╝ ██╗{Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝{Fore.WHITE} |
{Fore.WHITE} +---------------------------{Fore.CYAN}({Fore.RED}TorNetX{Fore.CYAN}){Fore.WHITE}---------------------------+
{Fore.WHITE} |{Fore.GREEN} Compatible with {Fore.CYAN}Windows{Fore.GREEN}, {Fore.CYAN}Mac{Fore.GREEN}, and {Fore.CYAN}Linux{Fore.GREEN} adapted by {Fore.CYAN}({Fore.RED}Macxzew{Fore.CYAN})  {Fore.WHITE}|
{Fore.WHITE} +---------------------------------------------------------------+{Style.RESET_ALL}
"""
    print(banner)
