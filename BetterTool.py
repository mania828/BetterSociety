
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich import box
import os
import time
from rich.live import Live
import socket
import getpass
import platform
import subprocess
import json
import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit,QPushButton, QLabel, QTextEdit, QStackedWidget


def show_Staff_menu():
    clear()
    console.print("STAFF MENU")

def show_rat_menu():
    clear()
    console.print("ADMIN MENU")

banned_ips = []
users = {}
current_user = None
#----start-----#


#----end-----#
console = Console()


def startup_warning():
    print("This tool is for educational use only.")
    choice = input("Do you want to continue? (y/n): ")

    if choice.lower() != "y":
        exit()
    

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    raw_art = """██████  ███████ ████████ ████████ ███████ ██████  ███████  ██████   ██████ ██ ███████ ████████ ██    ██
██   ██ ██         ██       ██    ██      ██   ██ ██      ██    ██ ██      ██ ██         ██     ██  ██ 
██████  █████      ██       ██    █████   ██████  ███████ ██    ██ ██      ██ █████      ██      ████   
██   ██ ██         ██       ██    ██      ██   ██      ██ ██    ██ ██      ██ ██         ██       ██    
██████  ███████    ██       ██    ███████ ██   ██ ███████  ██████   ██████ ██ ███████    ██       ██   

+ --------------------------------------------------------------------------------------------------- +
"""



    lines = raw_art.split("\n")
    rendered = [""] * len(lines)

    with Live(refresh_per_second=60, console=console) as live:
        for i, line in enumerate(lines):
            current = ""
            for char in line:
                current += char
                rendered[i] = current
                text = "\n".join(rendered)
                live.update(Align.center(Text(text, style="bold #A855F7")))
                time.sleep(0.003)

    lines = raw_art.split('\n')
    max_width = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_width) for line in lines]
    centered_art = '\n'.join(padded_lines)
    
    console.print(Align.center(Text(centered_art, style="bold #A855F7")))
    console.print()


console = Console()

current_user = None

FILE_PATH = os.path.join(os.path.dirname(__file__), "users.json")


def load_users():
    global users
    try:
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, "w") as f:
                json.dump({}, f)

        with open(FILE_PATH, "r") as f:
            users = json.load(f)

    except Exception as e:
        print("Load error:", e)
        users = {}


def save_users():
    try:
        with open(FILE_PATH, "w") as f:
            json.dump(users, f, indent=4)

    except Exception as e:
        print("Save error:", e)


def print_main_interface():
    clear()
    banner()
    console.print()
   

    # Spoofer Tools
    spoofer_table = Table(title="[ Spoofer Tools ]", title_style="bold #A855F7", 
                          box=box.SIMPLE_HEAVY, show_header=False, padding=(0, 2))
    spoofer_table.add_column("Command", style="bold cyan", width=12)
    spoofer_table.add_column("Description", style="bright_white")
    spoofer_table.add_row("!SMS", "Spoofs SMS")
    spoofer_table.add_row("!Discord", "Spoofs Discord")
    spoofer_table.add_row("!Telegram", "Spoofs Telegram")

    # DDoS Tools
    ddos_table = Table(title="[ DDoS Tools ]", title_style="bold #A855F7", 
                       box=box.SIMPLE_HEAVY, show_header=False, padding=(0, 2))
    ddos_table.add_column("Command", style="bold cyan", width=12)
    ddos_table.add_column("Description", style="bright_white")
    ddos_table.add_row("!ddos", "Launch powerful DDoS attacks")
    ddos_table.add_row("!layer7", "HTTP/HTTPS flood methods")
    ddos_table.add_row("!layer4", "UDP/TCP flood methods")

    # OSINT Tools
    osint_table = Table(title="[ OSINT Tools ]", title_style="bold #A855F7", 
                        box=box.SIMPLE_HEAVY, show_header=False, padding=(0, 2))
    osint_table.add_column("Command", style="bold cyan", width=14)
    osint_table.add_column("Description", style="bright_white")
    osint_table.add_row("!username <name>", "Username lookup across many sites")
    osint_table.add_row("!email <addr>", "Email OSINT & breach check")
    osint_table.add_row("!ip <address>", "IP address reconnaissance")
    osint_table.add_row("!domain <name>", "Domain & subdomain recon")

    Use_table = Table(title="[ How To use ]", title_style="bold #A855F7", 
                          box=box.SIMPLE_HEAVY, show_header=False, padding=(0, 2))
    Use_table.add_column("Command", style="bold cyan", width=12)
    Use_table.add_column("Description", style="bright_white")
    Use_table.add_row("!USE", "How to Use")
    Use_table.add_row("!Safe", "How to Keep Yourself Safe")
    Use_table.add_row("!Contact", "Contact The Dev")

    # Two-column layout
    left = Table.grid(padding=1)
    left.add_row(spoofer_table)
    left.add_row(Use_table)

    right = Table.grid(padding=1)
    right.add_row(ddos_table)
    right.add_row(osint_table)

    main_layout = Table.grid(padding=2)
    main_layout.add_row(left, right)

    console.print(Align.center(main_layout))

    # Command input area
    console.print()
    console.print("[bold #A855F7]Better Society v1.33[/]  [bold #A855F7] Made By BetterSociety[/] [bold #A855F7] 4K is my kitten[/] [dim]Type a command below[/]", 
                  style="dim", justify="center")
    console.print("[dim]──────────────────────────────────────────────────────────────[/]", justify="center")

def get_system_info():
    username = getpass.getuser()
    hostname = socket.gethostname()

    try:
        ip = socket.gethostbyname(hostname)
    except:
        ip = "Unknown"

    os_name = platform.system()

    return username, hostname, ip, os_name

def show_Staff_menu():
    clear()
    console.print(Align.center(Text(" STAFF MENU", style="bold #A855F7")))
    console.print()

    rat_table = Table(
        title="[ Staff Tools ]",
        title_style="bold #A855F7",
        box=box.SIMPLE_HEAVY,
        show_header=False,
        padding=(0, 2)
    )
    rat_table.add_column("Command", style="bold cyan", width=14)
    rat_table.add_column("Description", style="bright_white")

    rat_table.add_row("!BAN IP", "ip ban people")
    rat_table.add_row("!Kick", "Kick People")
    rat_table.add_row("!back", "Return to main menu")
    rat_table.add_row("INFO", "gives info of people")

    console.print(Align.center(rat_table))
    console.print()

    def show_rat_menu():
     clear()
     console.print(Align.center(Text(" ADMIN MENU", style="bold #A855F7")))
     console.print()

    rat_table = Table(
        title="[ Admin Tools ]",
        title_style="bold #A855F7",
        box=box.SIMPLE_HEAVY,
        show_header=False,
        padding=(0, 2)
    )
    rat_table.add_column("Command", style="bold cyan", width=14)
    rat_table.add_column("Description", style="bright_white")

    rat_table.add_row("!status", "Check system status")
    rat_table.add_row("!debug", "Debug info")
    rat_table.add_row("!back", "Return to main menu")
    rat_table.add_row("!webcam", "Open local webcam preview")

    console.print(Align.center(rat_table))
    console.print()


import cv2

def open_webcam():
    console.print("[green]Opening webcam... (press 'q' to close)[/]")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        console.print("[red]Could not access webcam[/]")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam Preview", frame)

        # press Q to close
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    console.print("[yellow]Webcam closed[/]")


def run_sherlock(username):
    sherlock_path = os.path.join(os.getcwd(), "sherlock")

    if not os.path.exists(sherlock_path):
        print("Sherlock folder not found:", sherlock_path)
        return

    subprocess.run(
        ["python", "sherlock.py", username],
        cwd=sherlock_path
    )



def handle_command(cmd: str):
    global current_user

    

    # ---------------- BASIC COMMANDS ---------------- #
    

    if cmd == "!sms":
        console.print("[#A855F7]not available now[/]")

    elif cmd == "!discord":
        console.print("[#A855F7]not available now[/]")
    
    elif cmd == "!register":
     register()

    elif cmd == "!login":
        if login():
            console.print("[green]Login success[/]")
        else:
            console.print("[red]Login failed[/]")

    elif cmd == "!whoami":
        if current_user:
            console.print(f"[green]Logged in as: {current_user}[/]")
        else:
            console.print("[red]Not logged in[/]")

    elif cmd == "!telegram":
        console.print("[#A855F7]not available now[/]")

    elif cmd == "!ddos":
        console.print("[#A855F7]not available now[/]")

    elif cmd == "!layer7":
        console.print("[#A855F7]not available now[/]")

    elif cmd == "!layer4":
        console.print("[#A855F7]not available now[/]")

    elif cmd.startswith("!email"):
        console.print("[#A855F7]not available now[/]")

    elif cmd.startswith("!ip"):
        console.print("[#A855F7]not available now[/]")

    elif cmd.startswith("!domain"):
        console.print("[#A855F7]not available now[/]")

    elif cmd == "!use":
        console.print("[#A855F7]start up the cmd the use the cmds[/]")

    elif cmd == "!safe":
        console.print("[#A855F7]Use Mullvad and ProxyChains4[/]")

    elif cmd == "!contact":
        console.print("[#A855F7]Add bettersociety on discord[/]")

    elif cmd.startswith("!username"):
        parts = cmd.split(" ", 1)
        if len(parts) < 2:
            console.print("[red]Usage: !username <name>[/]")
        else:
            run_sherlock(parts[1])

    # ---------------- STAFF MENU ---------------- #

    elif cmd == "!staff":
        console.print("[yellow]Enter Password to Access Staff Menu:[/]")
        password = getpass.getpass("! ")

        if password == "teeth":
            console.print("[green]Access Granted![/]")
            time.sleep(1)

            show_Staff_menu()

            while True:
                admin_cmd = console.input("[bold cyan]STAFF → [/]").strip().lower()

                if admin_cmd == "!back":
                    break

                elif admin_cmd == "!status":
                    console.print("[green]OK[/]")

                elif admin_cmd == "!debug":
                    console.print("[green]Debug active[/]")

                elif admin_cmd == "!webcam":
                    open_webcam()

                else:
                    console.print("[yellow]Unknown staff command[/]")

        else:
            console.print("[red]Wrong password[/]")

    # ---------------- ADMIN MENU ---------------- #

    elif cmd == "!admin":
        console.print("[yellow]Enter Password to Access Admin Menu:[/]")
        password = getpass.getpass("! ")

        if password == "4Kitten":
            console.print("[green]Access Granted![/]")
            time.sleep(1)

            show_rat_menu()

            while True:
                admin_cmd = console.input("[bold cyan]ADMIN → [/]").strip().lower()

                if admin_cmd == "!back":
                    break

                elif admin_cmd == "!status":
                    console.print("[green]System OK[/]")

                elif admin_cmd == "!debug":
                    console.print("[green]Debug active[/]")

                elif admin_cmd == "!webcam":
                    open_webcam()

                elif admin_cmd.startswith("!ban ip"):
                    parts = admin_cmd.split(" ")
                    if len(parts) < 3:
                        console.print("[red]Usage: !ban ip <ip>[/]")
                    else:
                        ip = parts[2]
                        banned_ips.append(ip)
                        console.print(f"[green]Banned IP: {ip}[/]")

                elif admin_cmd.startswith("!unban ip"):
                    parts = admin_cmd.split(" ")
                    if len(parts) < 3:
                        console.print("[red]Usage: !unban ip <ip>[/]")
                    else:
                        ip = parts[2]
                        if ip in banned_ips:
                            banned_ips.remove(ip)
                            console.print(f"[green]Unbanned IP: {ip}[/]")
                        else:
                            console.print("[yellow]IP not found[/]")

                elif admin_cmd == "!bans":
                    console.print(f"[cyan]{banned_ips}[/]")

                else:
                    console.print("[yellow]Unknown admin command[/]")

        else:
            console.print("[red]Wrong password[/]")

    # ---------------- FALLBACK ---------------- #

    else:
        console.print("[red]Unknown command[/]")

        


def main():
    console.print("[bold #A855F7]Better Society started successfully![/]\n")
    
    while True:
        print_main_interface()

        try:
            command = console.input("[bold cyan]→ [/]").strip()
            
            if command:
                handle_command(command)
            
            console.print()
            console.input("[dim]Press Enter to return to the main screen...[/]")
            
        except KeyboardInterrupt:
            console.print("\n[red]Use the X button on the window to properly close Better Society.[/]")
            time.sleep(1.5)
            continue
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/]")
            console.input("[dim]Press Enter to continue...[/]")
#-------------Login-----------------


def load_users():
    global users
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    except PermissionError:
        print("No permission to read users.json")
        users = {}

def save_users():
    try:
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
    except PermissionError:
        print("No permission to write users.json")
#----------password-----------


def register():
    load_users()

    username = input("Create username: ").strip()

    if username in users:
        print("User already exists")
        return

    password = input("Create password: ").strip()

    users[username] = {
        "password": password,
        "role": "user"
    }

    save_users()
    print("Account created successfully")


#-------------login----------------------


def login():
    global current_user

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in users and users[username]["password"] == password:
        current_user = username
        print(f"Logged in as {username}")
        return True
    else:
        print("Invalid login")
        return False
    

def is_admin():
    return current_user == "admin"



load_users()

load_users()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[red]Script failed: {e}[/]")
        input("Press Enter to exit...")
