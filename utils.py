from global_ import (
    data_file,
    user,
    SYS,
    os,
    json,
    sys,
    app_name,
    subprocess,
    logs_file,
    time,
    datetime,
    schedule,
    queue_file,
    config_file,
    default_config,
    enable_file,
    project_root,
    gitsync_branch
)
from colors import RED, RESET, GREEN, YELLOW, BLUE


def init():
    try:
        if not os.path.exists(project_root):
            print(f"{YELLOW}Creating root directory{RESET}")
        files = [logs_file, queue_file, config_file, data_file]
        for file in files:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    f.write("")
    except:
        print(f"{RED}Error initializing the tool{RESET}")
        sys.exit(1)


def check_for_git(dir_path):
    if not os.path.exists(f"{dir_path}/.git"):
        print(f"{RED}Not a git repository{RESET}")
        sys.exit(1)


def check_for_permissions(dir_path):
    if not os.access(dir_path, os.W_OK):
        print(f"{RED}Permission denied{RESET}")
        sys.exit(1)


def read():
    try:
        try:
            with open(data_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"{RED}File is corrupted{RESET}")
            allow_reset = input(
                f"{YELLOW}Do you want to reset the file and continue? (y/n){RESET}"
            )
            if allow_reset.lower() == "y":
                with open(data_file, "w") as f:
                    f.write("[]")
                print(f"{GREEN}File reset successfully{RESET}")
                return []
            else:
                print(f"{RED}Exiting...{RESET}")
                sys.exit(1)
    except FileNotFoundError:
        print(f"{RED}{data_file} not found, creating one...{RESET}")
        try:
            with open(data_file, "w") as f:
                f.write("[]")
            return []
        except:
            print(f"{RED}Error creating the file{RESET}")
        sys.exit(1)


def save(dirs):
    with open(data_file, "w") as f:
        json.dump(dirs, f)


def add(dir_):
    dirs = read()

    check_for_permissions(dir_)
    check_for_git(dir_)
    if dir_ not in dirs:
        dirs.append(dir_)
        save(dirs)
        print(f"{GREEN}{dir_} SET{RESET}")
    else:
        print(f"{YELLOW}{dir_} already inserted{RESET}")


def remove(dir):
    try:
        dirs = read()
        dirs.remove(dir)
        save(dirs)
        remove_from_queue(dir)
    except ValueError:
        print(f"{YELLOW}{dir} is not inserted{RESET}")


def prefix(dir_path):
    if dir_path == ".":
        return os.getcwd()
    elif dir_path == "..":
        return os.path.dirname(os.getcwd())
    elif dir_path == "~":
        return f"/home/{user}" if SYS == "LINUX" else f"C:\\Users\\{user}"
    print("Please use cd to the project you want to add and use 'add .'")
    exit(1)


def guard(argv):
    if len(argv) < 3:
        print(f"{RED}Missing argument{RESET}")
        sys.exit(1)
    dir_path = prefix(argv[2])
    if not os.path.exists(dir_path):
        print(f"{RED}Directory does not exist{RESET}")
        sys.exit(1)
    return dir_path


# -------------------------------------------------------------------------


def enable():
    try:
        if not os.path.exists(enable_file):
            os.system(f"touch {enable_file}")
    except:
        print(f"{RED}Error enabling the tool{RESET}")
        sys.exit(1)


def disable():
    try:
        if os.path.exists(enable_file):
            os.system(f"rm {enable_file}")
    except:
        print(f"{RED}Error disabling the tool{RESET}")
        sys.exit(1)


def is_active():
    try:
        return os.path.exists(enable_file)
    except:
        return False
    return False


# --------------------------------------------------------------------------
def Log(message):
    try:
        if not os.path.exists(logs_file):
            os.system(f"touch {logs_file}") if SYS == "LINUX" else os.system(
                f"echo. 2> {logs_file}"
            )
        with open(logs_file, "a") as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"{RED}Error logging the error{RESET}")


def handle_exception(e):
    Log("-" * 50)
    Log(e)
    Log("-" * 50)
    Log("\n")
    print("Error logged, check logs")


def push_to_origin(dir_, gitsync_branch_, origin_branch="main"):
    try:
        
        gitsync_branch_exists = subprocess.run(
            f"cd {dir_} && git branch --list {gitsync_branch_}",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        print(f"{GREEN}gitsync_branch_exists: {gitsync_branch_exists.stdout.decode().strip()}{RESET}")
        
        if gitsync_branch_exists.stdout.decode().strip():
            if not os.path.exists(f"{dir_}/.git"):
                print(f"{RED}Not a git repository{RESET}")
                raise Exception("Not a git repository")
            
            os.chdir(dir_)
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", read_commit_message()])
            subprocess.run(["git", "push", "origin", gitsync_branch_])
            subprocess.run(["git", "checkout", origin_branch])
            
        else:
            if not os.path.exists(f"{dir_}/.git"):
                print(f"{RED}Not a git repository{RESET}")
                raise Exception("Not a git repository")
            
            os.chdir(dir_)
            subprocess.run(["git", "checkout", "-B", gitsync_branch_])
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", read_commit_message()])
            subprocess.run(["git", "push", "origin", gitsync_branch_])
            subprocess.run(["git", "checkout", origin_branch])
            
    except Exception as e:
        print(f"{RED}{e}{RESET}")
        Log(str(time.ctime()) + " " + dir_)


def run(dirs=read()):
    count = 0
    if not is_active():
        print(f"Tool is disabled")
        sys.exit(1)

    if not dirs or len(dirs) == 0:
        Log(f"No directories yet")
        sys.exit(1)
    for dir_ in dirs:
        Log(f"\n>>>>>{dir_}<<<<<")
        try: 
            result = subprocess.run(
                f"cd {dir_} && git pull",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            Log(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            Log(str(time.ctime()) + " " + dir_)
            handle_exception(e.stderr.decode())
            Log(f"Try to pull manually")
            continue
        Log(f"{dir_} Up to date")
        try:
            
            current_branch = subprocess.run(
                f"cd {dir_} && git branch --show-current",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            origin_branch = current_branch.stdout.decode().strip()
            gitsync_branch_ = f"{gitsync_branch}{origin_branch}"
            push_to_origin(dir_, gitsync_branch_, origin_branch)
        except Exception as e:
            Log(str(time.ctime()) + " " + dir_)
            handle_exception(e)
            continue
        Log(f"{dir_} Syncronized at {time.ctime()}")
        count += 1

    final_message = f">>>>>{count}/{len(dirs)} syncronized without errors 🐫"
    Log(f"\n{final_message}")
    Log("-" * len(final_message))
    print(final_message)


# --------------------------------------------------------------------------
def config_interval(interval):
    valid_intervals = ["daily", "weekly", "monthly"]
    try:
        if int(interval) > 60:
            raise ValueError
    except ValueError:
        if interval not in valid_intervals:
            print(f"{RED}Invalid interval{RESET}")
            sys.exit(1)

    try:
        json_content = {"interval": interval, "commit_message": read_commit_message()}

        with open(config_file, "w") as f:
            json.dump(json_content, f)
        print(f"{GREEN}Config set{RESET}")
    except Exception as e:
        print(f"{RED}{e}{RESET}")


def read_interval():
    try:
        with open(config_file, "r") as f:
            return json.load(f)["interval"]
    except:
        print(f"{RED}File is corrupted{RESET}")
        allow_reset = input(
            f"{YELLOW}Do you want to reset the file and continue, the interval will be set to daily by default? (y/n){RESET}"
        )
        if allow_reset.lower() == "y":
            with open(config_file, "w") as f:
                f.write(default_config)
            print(f"{GREEN}File reset successfully with daily interval{RESET}")
            return "daily"
        else:
            print(f"{RED}Exiting...{RESET}")
            sys.exit(1)


def config_commit_message(message):
    try:
        json_content = {"interval": read_interval(), "commit_message": message}

        with open(config_file, "w") as f:
            json.dump(json_content, f)
        print(f"{GREEN}Config set{RESET}")
    except Exception as e:
        print(f"{RED}{e}{RESET}")


def read_commit_message():
    try:
        with open(config_file, "r") as f:
            return json.load(f)["commit_message"]
    except:
        print(f"{RED}File is corrupted{RESET}")
        allow_reset = input(
            f"{YELLOW}Do you want to reset the file and continue, the commit message will be set to 'Syncronized by gitsync' by default? (y/n){RESET}"
        )
        if allow_reset.lower() == "y":
            with open(config_file, "w") as f:
                f.write(default_config)
            print(f"{GREEN}File reset successfully with default commit message{RESET}")
            return "Syncronized by gitsync"
        else:
            print(f"{RED}Exiting...{RESET}")
            sys.exit(1)


# --------------------------------------------------------------------------
def add_to_queue(dir_path, time_should_run):
    try:
        with open(queue_file, "r") as f:
            data = json.load(f)
            data.append({"dir": dir_path, "time": time_should_run})
        with open(queue_file, "w") as f:
            json.dump(data, f)
    except:
        with open(queue_file, "w") as f:
            json.dump([{"dir": dir_path, "time": time_should_run}], f)


def remove_from_queue(dir_path):
    try:
        with open(queue_file, "r") as f:
            data = json.load(f)
            data = [item for item in data if item["dir"] != dir_path]
        with open(queue_file, "w") as f:
            json.dump(data, f)
    except:
        pass


def read_queue():
    try:
        with open(queue_file, "r") as f:
            return json.load(f)
    except:
        return []


def clear_queue():
    with open(queue_file, "w") as f:
        json.dump([], f)


def run_from_queue():
    dirs = read_queue()
    paths = [item["dir"] for item in dirs if item["time"] < time.time()]
    run(paths)
    clear_queue()


# --------------------------------------------------------------------------
def next_run(interval, duration=60):
    now = datetime.datetime.now()

    estimated_date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    Log(f"\nNext run will be at {estimated_date} \n")


def run_and_queue(duration=60):
    run_from_queue()
    now = datetime.datetime.now()
    target_time = now + datetime.timedelta(minutes=duration)
    dirs = read()
    for dir_ in dirs:
        add_to_queue(dir_, target_time.timestamp())
    next_run(read_interval(), duration)


def run_scheduler():
    Log(f"\nRunning queued tasks ⛰️\n")
    run_and_queue(-1)

    duration = 60
    interval = read_interval()

    Log(f"\nScheduler started with {interval} interval\n")

    try:
        if int(interval) < 60:
            duration = int(interval)
    except:
        pass
    if interval == "daily":
        duration = 60 * 24
    elif interval == "weekly":
        duration = 60 * 24 * 7
    elif interval == "monthly":
        duration = 60 * 24 * 30

    schedule.every(duration).minutes.do(run_and_queue, duration)

    while True:
        schedule.run_pending()
        time.sleep(1)
