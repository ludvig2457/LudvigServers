import os
import sys
import getpass
from colorama import Fore, Style, init
init(autoreset=True)

# ======== Настройка реальной файловой системы ========
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LudvigLinux")
home_dir = os.path.join(base_dir, "home")
etc_dir = os.path.join(base_dir, "etc")
var_dir = os.path.join(base_dir, "var")

def ensure_dirs(username="user"):
    """Создаёт необходимые реальные папки, если их нет"""
    os.makedirs(home_dir, exist_ok=True)
    os.makedirs(etc_dir, exist_ok=True)
    os.makedirs(var_dir, exist_ok=True)
    
    user_home = os.path.join(home_dir, username)
    os.makedirs(user_home, exist_ok=True)
    
    file_path = os.path.join(user_home, "file.txt")
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Welcome {username} to LudvigLinux! 🚀\n")
    
    config_path = os.path.join(etc_dir, "config.cfg")
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("config_version=1.0\n")

# ======== Основные команды ========
current_dir = base_dir
installed_packages = []
history = []

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

    # ===== Остальные команды =====
    elif command == "history":
        for i, h in enumerate(history, 1):
            print(f"{i}  {h}")

    elif command == "clear":
        os.system("cls" if os.name == "nt" else "clear")

    elif command == "exit" or command == "quit":
        sys.exit(0)

    elif command == "whoami":
        print("user")

    elif command == "neofetch":
        print(f"""
{Fore.CYAN}   .--.                  LudvigLinux
  |o_o |                 ----------------
  |:_/ |   User: user
 //   \\ \\  Host: LudvigLinux
(|     | ) Kernel: PythonOS
/\\_   _/\\  Packages: {len(installed_packages)}
\\__\\_/__/  Terminal: Python Virtual OS
{Style.RESET_ALL}""")

    else:
        print(f"{command}: command not found")

# ======== Основной цикл ========
def run():
    print(f"{Fore.YELLOW}Welcome to LudvigLinux virtual OS! Type 'help' for commands.{Style.RESET_ALL}")
    ensure_dirs()
    global current_dir
    current_dir = os.path.join(home_dir, "user")  # стартуем в домашней папке
    while True:
        try:
            prompt = f"{Fore.GREEN}user@LudvigLinux {Fore.BLUE}{current_dir}{Style.RESET_ALL}$ "
            command = input(prompt)
            run_command(command)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting LudvigLinux...")
            break

if __name__ == "__main__":
    run()
