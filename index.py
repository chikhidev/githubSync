from utils import read, add, remove, guard, is_active, enable, disable, run, run_scheduler, config_interval, config_commit_message, init
from global_ import user, SYS, os, json, sys, app_name, project_root, logs_file, queue_file, config_file, data_file
from colors import RED, RESET, GREEN, YELLOW, BLUE

def help_menu():
    print(f"{GREEN}Commands:{RESET}")
    print(f"{YELLOW}add, a, insert, i <directory>{RESET}")
    print(f"\tUsed to add a directory to the synchronization list")
    print(f"{YELLOW}remove, rm, delete, del <directory>{RESET}")
    print(f"\tUsed to remove a directory from the synchronization list")
    print(f"{YELLOW}list{RESET}")
    print(f"\tUsed to list all directories in the synchronization list")
    print(f"{YELLOW}enable{RESET}")
    print("\tUsed to enable the synchronization tool, when disabled it does not synchronize directories")
    print(f"{YELLOW}disable{RESET}")
    print("\tUsed to disable the synchronization tool, when disabled it does not synchronize directories")
    print(f"{YELLOW}config [-m, --message, -i, --interval]{RESET}")
    print(f"\tUsed to configure the synchronization tool\nCommit message: -m, --message\nInterval: -i, --interval")
    print(f"{YELLOW}run{RESET}")
    print(f"\tUsed to synchronize all directories")
    print(f"{YELLOW}run:scheduler{RESET}")
    print(f"\tUsed to synchronize all directories according to the configured interval, [daily, weekly, monthly]")
    
def warn_if_disabled(enabled):
    if not enabled and ["enable", "disable", "help"].count(command) == 0:
        print(f"{YELLOW}-{RESET}" * 66)
        print(f"{YELLOW}Tool is disabled: that means your directories are not synchronized{RESET}")
        print(f'{YELLOW}Use "{app_name} enable" to enable the tool{RESET}')
        print(f'{YELLOW}Or create a file named ".gitsync" in /home/{user} or C:\\Users\\{user} to enable it{RESET}')
        print(f"{YELLOW}-{RESET}" * 66)

if __name__ == '__main__':
    try:
        if not SYS == "LINUX":
            print(f"{RED}This tool is only available for Linux i am sorry...{RESET}")
            sys.exit(1)
            
        init()
            
        enabled = is_active()
        
        if len(sys.argv) == 1:
            if enabled:
                print(f"{YELLOW}By default, calling run:scheduler{RESET}")
                run_scheduler()
            else:
                print(f"{YELLOW}The tool is disabled, use 'enable' to enable it{RESET}")
                sys.exit(1)
            sys.exit(0)

        command = sys.argv[1]

        warn_if_disabled(enabled)

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
            index = 1
            for dir in dirs:
                print(f"---@{index} {BLUE}{dir}{RESET}")
                index += 1
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
        elif command == "config":
            if len(sys.argv) < 3:
                print(f"{RED}Missing specifier [-m, --message, -i, --interval]{RESET}")
                sys.exit(1)
            specifier = sys.argv[2]
            if specifier == "-i" or specifier == "--interval":
                if len(sys.argv) < 4:
                    print(f"{RED}Missing interval argument [NUMBER, daily, weekly, monthly]{RESET}")
                    sys.exit(1)
                config_interval(sys.argv[3])
            elif specifier == "-m" or specifier == "--message":
                if len(sys.argv) < 4:
                    print(f"{RED}Missing message argument{RESET}")
                    sys.exit(1)
                config_commit_message(sys.argv[3])
            else:
                print(f"{RED}Invalid specifier{RESET}")
                sys.exit(1)
        elif command == "run":
            run()
        elif command == "run:scheduler":
            run_scheduler()
        elif command == "init":
            init()
        elif command == "version" or command == "--version" or command == "-v":
            print(f"{GREEN}Version: 1.0.0{RESET}")
        elif command == "status":
            if enabled:
                print(f"{GREEN}Tool is enabled{RESET}")
            else:
                print(f"{YELLOW}Tool is disabled{RESET}")
        elif command == "logs":
            os.system(f"open {logs_file}")
        elif command == "logs:clear":
            with open(logs_file, "w") as f:
                f.write("")
            print(f"{GREEN}Logs cleared{RESET}")
        elif command == "help":
            help_menu()
        else:
            print(f"{RED}Invalid command{RESET}")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"{RED}Exiting...{RESET}")
        sys.exit(1)
