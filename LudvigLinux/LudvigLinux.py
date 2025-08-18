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
current_user = None
current_dir = None

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
    global current_dir
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

    # ===== Прочие команды =====
    elif command == "history":
        for i, h in enumerate(history, 1):
            print(f"{i}  {h}")

    elif command == "clear":
        os.system("cls" if os.name == "nt" else "clear")

    elif command in ["exit", "quit"]:
        sys.exit(0)

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

    elif command == "help":
        print("Commands: ls, cd, pwd, cat, touch, mkdir, rm, history, clear, whoami, neofetch, exit")

    else:
        print(f"{command}: command not found")

# ======== Основной цикл ========
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
