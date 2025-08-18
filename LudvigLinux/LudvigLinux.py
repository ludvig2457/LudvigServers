import os
import sys
import getpass
from colorama import Fore, Style, init
init(autoreset=True)

# ======== Настройка базовой директории ========
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LudvigLinux")
HOME_DIR = os.path.join(BASE_DIR, "home")
ETC_DIR = os.path.join(BASE_DIR, "etc")
VAR_DIR = os.path.join(BASE_DIR, "var")

installed_packages = []
history = []
processes = {1: "init", 2: "bash", 3: "htop"}
services = {"ssh": False, "nginx": False, "mysql": False}

current_user = None
current_dir = None
next_pid = 4

# ======== Функции ========
def create_system(username, password):
    """Создаёт реальную структуру LudvigLinux с пользователем"""
    global current_user, current_dir
    current_user = username
    os.makedirs(os.path.join(HOME_DIR, username), exist_ok=True)
    os.makedirs(ETC_DIR, exist_ok=True)
    os.makedirs(VAR_DIR, exist_ok=True)

    # приветственный файл
    user_file = os.path.join(HOME_DIR, username, "welcome.txt")
    with open(user_file, "w", encoding="utf-8") as f:
        f.write(f"Welcome {username} to LudvigLinux! 🚀\n")

    # базовый конфиг
    config_file = os.path.join(ETC_DIR, "config.cfg")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("config_version=1.0\n")

    current_dir = os.path.join(HOME_DIR, username)
    print(f"LudvigLinux installed! User '{username}' home: {current_dir}")

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
        for pid, proc in processes.items():
            print(f"{pid:<5} {proc}")

    elif command == "kill":
        if len(args) < 2:
            print("kill: missing pid")
        else:
            try:
                pid = int(args[1])
                if pid in processes:
                    print(f"Killed process {pid} ({processes[pid]})")
                    del processes[pid]
                else:
                    print(f"kill: {pid}: no such process")
            except ValueError:
                print("kill: pid must be a number")

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
        else:
            op = args[1]
            if op == "-S" and len(args) > 2:
                pkg = args[2]
                installed_packages.append(pkg)
                print(f":: installing {pkg}... [DONE]")
            elif op == "-Qs":
                if installed_packages:
                    print("\n".join([f"local/{pkg} 1.0-1" for pkg in installed_packages]))
                else:
                    print("No packages installed.")
            elif op == "-Syu":
                print(":: Synchronizing package databases...")
                print(" core            134.5 KiB  125K/s 00:01 [################] 100%")
                print(" extra          1630.2 KiB  500K/s 00:03 [################] 100%")
                print(" community      5123.4 KiB  1.2M/s 00:04 [################] 100%")
                print(":: Starting full system upgrade...")
                print(" nothing to do")
            else:
                print(f"pacman: unknown operation {op}")

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

    elif command == "shutdown":
        print("System shutting down...")
        sys.exit(0)

    elif command == "reboot":
        print("System rebooting...")
        os.execv(sys.executable, ["python"] + sys.argv)

    elif command == "help":
        print("Commands: ls, cd, pwd, cat, touch, mkdir, rm, ps, kill, systemctl, pacman, history, clear, whoami, neofetch, reboot, shutdown, exit")

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
