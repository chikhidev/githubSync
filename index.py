from utils import check_for_git, read, save, add, remove, prefix, guard, is_active, enable, disable, run
from global_ import data_file, user, SYS, os, json, sys, app_name
from colors import RED, RESET, GREEN, YELLOW, BLUE

if __name__ == '__main__':
    try:
        if not SYS == "LINUX":
            print(f"{RED}This tool is only available for Linux :( i am sorry...{RESET}")
            sys.exit(1)

        if not os.path.exists(data_file):
            with open(data_file, 'w') as f:
                f.write("[]")

        if len(sys.argv) == 1:
            print(f"{YELLOW}Use '{app_name} help' to see the available commands{RESET}")
            sys.exit(1)

        command = sys.argv[1]

        enabled = is_active()
        if not enabled and ["enable", "disable", "help"].count(command) == 0:
            print(f"{YELLOW}-{RESET}" * 66)
            print(f"{YELLOW}Tool is disabled: that means your directories are not synchronized{RESET}")
            print(f'{YELLOW}Use "{app_name} enable" to enable the tool{RESET}')
            print(f'{YELLOW}Or create a file named ".gitsync" in /home/{user} or C:\\Users\\{user} to enable it{RESET}')
            print(f"{YELLOW}-{RESET}" * 66)

        if command == "add" or command == "a" or command == "insert" or command == "i":
            dir_path = guard(sys.argv)
            add(dir_path)
        elif command == "remove" or command == "rm" or command == "delete" or command == "del":
            dir_path = guard(sys.argv)
            remove(dir_path)
        elif command == "list":
            dirs = read()
            if not dirs or len(dirs) == 0:
                print(f"{YELLOW}No directories yet{RESET}")
                sys.exit(1)
            print(f"{GREEN}Directories:{RESET}")
            for dir in dirs:
                print(f"---{BLUE}{dir}{RESET}")
        elif command == "enable":
            if not enabled:
                enable()
            else:
                print(f"{YELLOW}Tool is already enabled{RESET}")
        elif command == "disable":
            if enabled:
                disable()
            else:
                print(f"{YELLOW}Tool is already disabled{RESET}")
        elif command == "run":
            run()
        else:
            print(f"{RED}Invalid command{RESET}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"{RED}Exiting...{RESET}")
        sys.exit(1)
