from colorama import init, Fore, Style

# Initialiser colorama pour Windows et Linux
init(autoreset=True)

# Bannière
def print_banner():
    banner = f"""
{Fore.WHITE} +-------------------------------------------------------+
{Fore.WHITE} |{Fore.GREEN} ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗{Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN} ╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝{Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   {Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   {Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   {Fore.WHITE} |
{Fore.WHITE} |{Fore.GREEN}    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   {Fore.WHITE} |
{Fore.WHITE} +---------------------{Fore.CYAN}({Fore.RED}ByteBreach{Fore.CYAN}){Fore.WHITE}----------------------+
{Fore.WHITE} |{Fore.GREEN} Compatible with {Fore.CYAN}Windows {Fore.GREEN}and {Fore.WHITE}Mac{Fore.GREEN}, adapted by {Fore.CYAN}({Fore.RED}Macxzew{Fore.CYAN}){Fore.GREEN} {Fore.WHITE}|
{Fore.WHITE} +-------------------------------------------------------+{Style.RESET_ALL}
"""
    print(banner)
