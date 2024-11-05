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
def Log(message, end="\n"):
    try:
        if not os.path.exists(logs_file):
            os.system(f"touch {logs_file}")
        with open(logs_file, "a") as f:
            f.write(f"{message}" + end)
    except Exception as e:
        print(f"{RED}Error logging the error{RESET}")


def handle_exception(e):
    Log(e)
    Log("\n")
    print("Error logged, check logs")


def push_to_origin(dir_, gitsync_branch_, origin_branch="main"):
    """
    Pushes changes from the gitsync_branch_ to the origin_branch in the given directory.
    
    Args:
        dir_ (str): The directory containing the Git repository.
        gitsync_branch_ (str): The branch to push changes from.
        origin_branch (str, optional): The branch to push changes to. Defaults to "main".
    """
    try:
        gitsync_branch_exists = subprocess.run(
            ["git", "branch", "--list", gitsync_branch_],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        Log(f"gitsync_branch_exists: {gitsync_branch_exists.stdout.decode().strip()}")
        
        if not os.path.exists(f"{dir_}/.git"):
            Log(f"Error: Not a git repository")
            raise Exception("Not a git repository")
        
        os.chdir(dir_)
        
        if gitsync_branch_exists.stdout.decode().strip():

            Log(f"Checking out {origin_branch} branch")
            subprocess.run(["git", "checkout", origin_branch], check=True)

            Log("Adding all changes")
            subprocess.run(["git", "add", "."], check=True)

            Log(f"Committing changes with message: '{read_commit_message()} merge at {time.ctime()}'")
            subprocess.run(["git", "commit", "-m", read_commit_message() + " merge at " + time.ctime()], check=True)

            Log(f"Checking out {gitsync_branch_} branch")
            subprocess.run(["git", "checkout", gitsync_branch_], check=True)

            Log(f"Merging {origin_branch} into {gitsync_branch_}")
            subprocess.run(["git", "merge", origin_branch, "--strategy-option=theirs"], check=True)

            Log(f"Pushing {gitsync_branch_} to origin")
            subprocess.run(["git", "push", "--set-upstream", "origin", gitsync_branch_], check=True)
            
        else:

            Log(f"Checking out {origin_branch} branch")
            subprocess.run(["git", "checkout", origin_branch], check=True)
            
            Log(f"Creating and checking out {gitsync_branch_} branch")
            subprocess.run(["git", "checkout", "-B", gitsync_branch_], check=True)
            
            Log(f"Pushing {gitsync_branch_} to origin (force)")
            subprocess.run(["git", "add", "."])
            
            Log(f"Committing initial commit with message: '[{read_commit_message()}] Initial commit at {time.ctime()}'")
            subprocess.run(["git", "commit", "-m", "[" + read_commit_message() + "] Initial commit at " + time.ctime()], check=True)
            
            Log(f"Pushing {gitsync_branch_} to origin (force)")
            subprocess.run(["git", "push", "origin", gitsync_branch_, "--force"], check=True)
            
            Log(f"Checking out {origin_branch} branch")
            subprocess.run(["git", "checkout", origin_branch], check=True)
    except Exception as e:
        Log(f"Error throwed: {e} [push_to_origin]")
        subprocess.run(["git", "checkout", origin_branch], check=True)

def run(dirs=read()):
    """
    Runs the push_to_origin function for each directory in the dirs list.
    
    Args:
        dirs (list, optional): A list of directories to process. Defaults to read().
    """
    count = 0
    if not is_active():
        Log("Tool is disabled")
        sys.exit(1)

    if not dirs or len(dirs) == 0:
        Log("No directories to run")
        return
    for dir_ in dirs:
        msg = f"| {dir_} |"
        Log("")
        Log("+", "")
        Log("-" * (len(msg) - 2), "")
        Log("+")
        Log(msg)
        Log("+", "")
        Log("-" * (len(msg) - 2), "")
        Log("+")

        current_branch = subprocess.run(
            f"cd {dir_} && git branch --show-current",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try: 
            os.chdir(dir_)

            Log(f"Pulling latest changes from {current_branch.stdout.decode().strip()} branch")
            result = subprocess.run(
                ["git", "pull", "origin", current_branch.stdout.decode().strip()],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            Log(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            Log("Try to pull manually in the directory: " + dir_)
            subprocess.run(["notify-send", f"gitsync: unable to pull in {dir_}"])
            continue
        Log(f"{dir_} is up to date")
        try:            
            origin_branch = current_branch.stdout.decode().strip()
            gitsync_branch_ = f"{gitsync_branch}{origin_branch}"
            push_to_origin(dir_, gitsync_branch_, origin_branch)
        except Exception as e:
            Log(f"Error in directory: {dir_}")
            subprocess.run(["notify-send", f"gitsync: error in {dir_}"])
            handle_exception(e)
            continue
        Log(f"{dir_} synchronized")
        count += 1

    final_message = f"{count}/{len(dirs)} directories synchronized without errors 🐫"
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
    Log(f"Running queued tasks ⛰️ " + time.ctime())
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
