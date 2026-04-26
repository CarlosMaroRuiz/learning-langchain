import os
import sys
import time
import pyfiglet
from colorama import Fore, Style, init
P
init()


def create_banner(text: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    boot_sequence = [
        "[*] INICIALIZANDO SISTEMA NEURAL...",
        "[*] BYPASS DE PROTOCOLOS DE SEGURIDAD... [OK]",
        "[*] ESTABLECIENDO CONEXIÓN CON NODO CENTRAL...",
        "[*] CARGANDO MODELOS LLM..."
    ]
    
    for line in boot_sequence:
        sys.stdout.write(Fore.GREEN + Style.DIM + line + "\n" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.3) 
    print()

    ascii_text = pyfiglet.figlet_format(text, font="slant")
    lines = ascii_text.split('\n')
    size = max(len(line) for line in lines) if lines else 0
    
    print(Fore.GREEN + Style.BRIGHT + "═" * size + Style.RESET_ALL)
    
    for line in lines:
        sys.stdout.write(Fore.GREEN + Style.BRIGHT + line + "\n" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.05) 
        
    print(Fore.GREEN + Style.BRIGHT + "═" * size + Style.RESET_ALL)
    print(Fore.GREEN + ">>> ESPERANDO INPUT..." + Style.RESET_ALL)
    print()

def create_banner_ultra(text: str,art: str):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    boot_sequence = [
        "[*] INICIALIZANDO INTERFAZ... [OK]",
        "[*] CARGANDO MÓDULO DE CONCIENCIA... [OK]",
        "[*] SISTEMA CARGADO... [OK]"
    ]
    
    for line in boot_sequence:
        sys.stdout.write(Fore.CYAN + Style.DIM + line + "\n" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.3) 
    print()

    
    for line in art.split('\n'):
        sys.stdout.write(Fore.CYAN + Style.BRIGHT + line + "\n" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.05)
        
    print()

    ascii_text = pyfiglet.figlet_format(text, font="slant")
    lines = ascii_text.split('\n')
    size = max(len(line) for line in lines) if lines else 0
    
    print(Fore.CYAN + Style.BRIGHT + "═" * size + Style.RESET_ALL)
    
    for line in lines:
        sys.stdout.write(Fore.CYAN + Style.BRIGHT + line + "\n" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.05) 
        
    print(Fore.CYAN + Style.BRIGHT + "═" * size + Style.RESET_ALL)
    print(Fore.CYAN + ">>> AGENTE CONECTADO. ESPERANDO INPUT..." + Style.RESET_ALL)
    print()
