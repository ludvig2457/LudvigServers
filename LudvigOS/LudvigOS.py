import os
import sys
import getpass
import urllib.request
import time
import random
import subprocess
from colorama import Fore, Style, init
init(autoreset=True)

# ======== Настройка базовой директории ========
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LudvigLinux")
HOME_DIR = os.path.join(BASE_DIR, "home")
ETC_DIR = os.path.join(BASE_DIR, "etc")
VAR_DIR = os.path.join(BASE_DIR, "var")
APPS_DIR = os.path.join(BASE_DIR, "apps")

installed_packages = []
history = []
processes = {
    1: {"name": "init", "cpu": 0, "mem": 0},
    2: {"name": "bash", "cpu": 0, "mem": 0},
    3: {"name": "htop", "cpu": 0, "mem": 0}
}
services = {"ssh": False, "nginx": False, "mysql": False}

current_user = None
current_dir = None
next_pid = 4
start_time = time.time()

GITHUB_URL = "https://raw.githubusercontent.com/ludvig2457/LudvigServers/main/LudvigOS/LudvigOS.py"
GUI_URL = "https://raw.githubusercontent.com/ludvig2457/LudvigServers/main/LudvigOS/LudvigOSGUI.py"

# ======== Функции ========
def create_system(username, password):
    global current_user, current_dir
    current_user = username
    os.makedirs(os.path.join(HOME_DIR, username), exist_ok=True)
    os.makedirs(ETC_DIR, exist_ok=True)
    os.makedirs(VAR_DIR, exist_ok=True)
    os.makedirs(APPS_DIR, exist_ok=True)

    user_file = os.path.join(HOME_DIR, username, "welcome.txt")
    with open(user_file, "w", encoding="utf-8") as f:
        f.write(f"Welcome {username} to LudvigLinux! 🚀\n")

    config_file = os.path.join(ETC_DIR, "config.cfg")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("config_version=1.0\n")

    current_dir = os.path.join(HOME_DIR, username)
    print(f"LudvigLinux installed! User '{username}' home: {current_dir}")

def download_with_progress(url, local_path):
    """Скачивает файл с прогресс-баром"""
    print(f"{Fore.CYAN}Downloading...{Style.RESET_ALL}")
    try:
        response = urllib.request.urlopen(url)
        total = int(response.getheader('Content-Length').strip())
        downloaded = 0
        block_size = 8192
        with open(local_path, 'wb') as f:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                f.write(buffer)
                done = int(40 * downloaded / total)
                sys.stdout.write(f"\r[{Fore.GREEN}{'#' * done}{Style.RESET_ALL}{'-' * (40 - done)}] "
                                 f"{downloaded * 100 // total}%")
                sys.stdout.flush()
        print(f"\n{Fore.GREEN}Download completed!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"\n{Fore.RED}Download failed: {e}{Style.RESET_ALL}")
        return False

def update_ludviglinux():
    local_path = os.path.abspath(sys.argv[0])
    backup_path = local_path + ".bak"
    try:
        os.rename(local_path, backup_path)
        print(f"{Fore.YELLOW}Old version backed up.{Style.RESET_ALL}")
        time.sleep(0.5)
        success = download_with_progress(GITHUB_URL, local_path)
        if success:
            print(f"{Fore.GREEN}Old version removed.{Style.RESET_ALL}")
            os.remove(backup_path)
            print(f"{Fore.GREEN}Restarting LudvigLinux...{Style.RESET_ALL}")
            os.execv(sys.executable, ["python"] + [local_path])
        else:
            print(f"{Fore.RED}Update failed, restoring old version...{Style.RESET_ALL}")
            os.rename(backup_path, local_path)
    except Exception as e:
        print(f"{Fore.RED}Update error: {e}{Style.RESET_ALL}")
        if os.path.exists(backup_path):
            os.rename(backup_path, local_path)

def nano_editor(filename):
    path = os.path.join(current_dir, filename)
    content = ""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    print(f"{Fore.YELLOW}-- NANO EDITOR: {filename} -- (type ':wq' to save and exit){Style.RESET_ALL}")
    lines = content.splitlines()
    while True:
        for i, line in enumerate(lines):
            print(f"{i+1}: {line}")
        inp = input()
        if inp == ":wq":
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print(f"{Fore.GREEN}File saved.{Style.RESET_ALL}")
            break
        else:
            lines.append(inp)

def update_processes():
    for pid, proc in processes.items():
        proc["cpu"] = random.randint(0, 50)
        proc["mem"] = random.randint(0, 50)

def run_command(cmd):
    global current_dir, next_pid
    args = cmd.strip().split()
    if not args:
        return
    command = args[0]
    history.append(cmd)

    # ===== Файловые команды =====
    if command == "ls":
        try:
            print("  ".join(os.listdir(current_dir)))
        except FileNotFoundError:
            print(f"ls: cannot access '{current_dir}'")

    elif command == "cd":
        if len(args) < 2:
            print("cd: missing operand")
        else:
            path = args[1]
            new_path = os.path.join(current_dir, path) if not path.startswith("/") else path
            if os.path.isdir(new_path):
                current_dir = os.path.abspath(new_path)
            else:
                print(f"cd: no such file or directory: {path}")

    elif command == "pwd":
        print(current_dir)

    elif command == "cat":
        if len(args) < 2:
            print("cat: missing file operand")
        else:
            path = os.path.join(current_dir, args[1])
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    print(f.read(), end="")
            else:
                print(f"cat: {args[1]}: No such file")

    elif command == "touch":
        if len(args) < 2:
            print("touch: missing file operand")
        else:
            path = os.path.join(current_dir, args[1])
            open(path, "a").close()

    elif command == "mkdir":
        if len(args) < 2:
            print("mkdir: missing operand")
        else:
            path = os.path.join(current_dir, args[1])
            os.makedirs(path, exist_ok=True)

    elif command == "rm":
        if len(args) < 2:
            print("rm: missing operand")
        else:
            path = os.path.join(current_dir, args[1])
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                try:
                    os.rmdir(path)
                except OSError:
                    print(f"rm: cannot remove '{args[1]}', directory not empty")
            else:
                print(f"rm: cannot remove '{args[1]}', no such file or directory")

    # ===== Процессы =====
    elif command == "ps":
        update_processes()
        print(f"{'PID':<5} {'Name':<10} {'CPU%':<5} {'MEM%':<5}")
        for pid, proc in processes.items():
            print(f"{pid:<5} {proc['name']:<10} {proc['cpu']:<5} {proc['mem']:<5}")

    elif command == "top":
        update_processes()
        print(f"{'PID':<5} {'Name':<10} {'CPU%':<5} {'MEM%':<5}")
        for pid, proc in processes.items():
            bar_cpu = "#" * (proc["cpu"] // 2)
            bar_mem = "#" * (proc["mem"] // 2)
            print(f"{pid:<5} {proc['name']:<10} CPU:[{bar_cpu:<25}] MEM:[{bar_mem:<25}]")

    elif command == "kill":
        if len(args) < 2:
            print("kill: missing pid")
        else:
            try:
                pid = int(args[1])
                if pid in processes:
                    print(f"Killed process {pid} ({processes[pid]['name']})")
                    del processes[pid]
                else:
                    print(f"kill: {pid}: no such process")
            except ValueError:
                print("kill: pid must be a number")

    # ===== Мини-редактор =====
    elif command == "nano":
        if len(args) < 2:
            print("Usage: nano <filename>")
        else:
            nano_editor(args[1])

    # ===== Сервисы =====
    elif command == "systemctl":
        if len(args) < 3:
            print("systemctl: usage: systemctl <start|stop|status> <service>")
        else:
            action, service = args[1], args[2]
            if service not in services:
                print(f"systemctl: {service}: not found")
            else:
                if action == "start":
                    services[service] = True
                    print(f"Started {service}.service")
                elif action == "stop":
                    services[service] = False
                    print(f"Stopped {service}.service")
                elif action == "status":
                    status = "active (running)" if services[service] else "inactive (dead)"
                    print(f"{service}.service - Fake service\n   Loaded: loaded\n   Active: {status}")
                else:
                    print(f"systemctl: unknown action {action}")

    # ===== pacman =====
    elif command == "pacman":
        if len(args) < 2:
            print("pacman: missing operation")
            return
        op = args[1]

        # Установка пакета
        if op == "-S" and len(args) > 2:
            pkg = args[2]
            if pkg not in installed_packages:
                installed_packages.append(pkg)
            print(f":: installing {pkg}... [DONE]")

            # Специально для VS Code
            if pkg == "code":
                code_path = os.path.join(BASE_DIR, "apps", "VSCodeSetup.exe")
                os.makedirs(os.path.dirname(code_path), exist_ok=True)
                if not os.path.exists(code_path):
                    url = "https://update.code.visualstudio.com/latest/win32-x64-user/stable"
                    print(f"{Fore.CYAN}Downloading {pkg}...{Style.RESET_ALL}")
                    if download_with_progress(url, code_path):
                        print(f"{Fore.GREEN}VS Code downloaded! Launch with 'code'{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Failed to download VS Code.{Style.RESET_ALL}")

        # Удаление пакета
        elif op == "-R" and len(args) > 2:
            pkg = args[2]
            if pkg in installed_packages:
                installed_packages.remove(pkg)
                print(f":: removed {pkg}... [DONE]")
            else:
                print(f"pacman: {pkg} is not installed")

        # Синхронизация базы
        elif op == "-Sy":
            print(":: Synchronizing package databases...")
            time.sleep(0.5)
            print(":: Database updated!")

        # Полное обновление системы
        elif op == "-Syu":
            print(":: Synchronizing package databases...")
            time.sleep(0.5)
            print(":: Starting full system upgrade...")
            for pkg in installed_packages:
                print(f":: upgrading {pkg}... [DONE]")
                time.sleep(0.2)
            update_ludviglinux()

        # Поиск установленных пакетов
        elif op == "-Qs":
            if installed_packages:
                print("\n".join([f"local/{pkg} 1.0-1" for pkg in installed_packages]))
            else:
                print("No packages installed.")

        else:
            print(f"pacman: unknown operation {op}")

    # ===== Запуск реальных приложений =====
    elif command == "code":
        code_path = os.path.join(BASE_DIR, "apps", "VSCodeSetup.exe")
        if os.path.exists(code_path):
            print(f"{Fore.GREEN}Launching VS Code...{Style.RESET_ALL}")
            os.startfile(code_path)
        else:
            print(f"{Fore.RED}VS Code is not installed. Use 'pacman -S code'{Style.RESET_ALL}")

    # ===== GUI =====
    elif command == "gui":
        gui_file = os.path.join(BASE_DIR, "LudvigOSGUI.py")
        if not os.path.exists(gui_file):
            print("GUI not found. Downloading...")
            if download_with_progress(GUI_URL, gui_file):
                print("GUI downloaded successfully.")
            else:
                print("Failed to download GUI.")
                return
        print("Launching GUI...")
        try:
            os.system(f"{sys.executable} {gui_file}")
            print("Returned from GUI.")
        except Exception as e:
            print(f"Error launching GUI: {e}")

    # ===== Прочее =====
    elif command == "history":
        for i, h in enumerate(history, 1):
            print(f"{i}  {h}")

    elif command == "clear":
        os.system("cls" if os.name == "nt" else "clear")

    elif command == "whoami":
        print(current_user)

    elif command == "neofetch":
        print(f"""
{Fore.CYAN}   .--.                  LudvigLinux
  |o_o |                 ----------------
  |:_/ |   User: {current_user}
 //   \\ \\  Host: LudvigLinux
(|     | ) Kernel: PythonOS
/\\_   _/\\  Packages: {len(installed_packages)}
\\__\\_/__/  Terminal: Python Virtual OS
{Style.RESET_ALL}""")

    elif command == "uptime":
        elapsed = int(time.time() - start_time)
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Uptime: {hours}h {minutes}m {seconds}s")

    elif command == "shutdown":
        print("System shutting down...")
        sys.exit(0)

    elif command == "reboot":
        print("System rebooting...")
        os.execv(sys.executable, ["python"] + sys.argv)

    elif command == "help":
        print("Commands: ls, cd, pwd, cat, touch, mkdir, rm, ps, top, kill, nano, systemctl, pacman, code, history, clear, whoami, neofetch, uptime, gui, reboot, shutdown, exit")

    else:
        print(f"{command}: command not found")

# ===== Основный цикл =====
def run():
    print(f"{Fore.YELLOW}Welcome to LudvigLinux installer!{Style.RESET_ALL}")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    create_system(username, password)

    print(f"{Fore.GREEN}Starting virtual LudvigLinux shell...{Style.RESET_ALL}")
    while True:
        try:
            prompt = f"{Fore.GREEN}{current_user}@LudvigLinux {Fore.BLUE}{current_dir}{Style.RESET_ALL}$ "
            command = input(prompt)
            run_command(command)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting LudvigLinux...")
            break

if __name__ == "__main__":
    run()
