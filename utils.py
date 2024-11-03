from global_ import data_file, user, SYS, os, json, sys, app_name, subprocess, logs_file, time, datetime, schedule, queue_file, config_file
from colors import RED, RESET, GREEN, YELLOW, BLUE

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
        with open(data_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}File is corrupted{RESET}")
        allow_reset = input(f"{YELLOW}Do you want to reset the file and continue? (y/n){RESET}")
        if allow_reset.lower() == "y":
            with open(data_file, 'w') as f:
                f.write("[]")
            print(f"{GREEN}File reset successfully{RESET}")
            return []
        else:
            print(f"{RED}Exiting...{RESET}")
            sys.exit(1)

def save(dirs):
    with open(data_file, 'w') as f:
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
    except ValueError:
        print(f"{YELLOW}{dir} is not inserted{RESET}")

def prefix(dir_path):
    if dir_path == ".":
        return os.getcwd()
    elif dir_path == "..":
        return os.path.dirname(os.getcwd())
    elif dir_path == "~":
        return f"/home/{user}" if SYS == "LINUX" else f"C:\\Users\\{user}"
    return dir_path

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
        if SYS == "LINUX":
            os.system(f"touch /home/{user}/.gitsync")
        else:
            os.system(f"echo. 2> C:\\Users\\{user}\\.gitsync")
    except:
        print(f"{RED}Error enabling the tool{RESET}")
        sys.exit(1)

def disable():
    try:
        if SYS == "LINUX":
            os.system(f"rm /home/{user}/.gitsync")
        else:
            os.system(f"del C:\\Users\\{user}\\.gitsync")
    except:
        print(f"{RED}Error disabling the tool{RESET}")
        sys.exit(1)

def is_active():
    try:
        if SYS == "LINUX":
            return os.path.exists(f"/home/{user}/.gitsync")
        else:
            return os.path.exists(f"C:\\Users\\{user}\\.gitsync")
    except:
        return False
    return False

#--------------------------------------------------------------------------
def Log(message):
    try:
        if not os.path.exists(logs_file):
            os.system(f"touch {logs_file}") if SYS == "LINUX" else os.system(f"echo. 2> {logs_file}")
        with open(logs_file, 'a') as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"{RED}Error logging the error{RESET}")

def handle_exception(e):
    Log('-' * 50)
    Log(e)
    Log('-' * 50)
    Log('\n')
    print("Error logged, check logs")

def push_to_origin(branch):
    try:
        os.system(f"cd {dir}")
        os.system("git add .")
        os.system(f"git commit -m 'Syncronized by {app_name}'")
        if branch:
            os.system(f"git push origin {branch}")
        else:
            os.system("git push")
    except Exception as e:
        print(f"{RED}{e}{RESET}")

def run():
    Log("-" * 50)
    count = 0
    if not is_active():
        print(f"Tool is disabled")
        sys.exit(1)
    dirs = read()
    if not dirs or len(dirs) == 0:
        Log(f"No directories yet")
        sys.exit(1)
    for dir in dirs:
        Log(f">>>>>{dir}")
        try:
            result = subprocess.run(f"cd {dir} && git pull", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            Log(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            Log(str(time.ctime()) + " " + dir)
            handle_exception(e.stderr.decode())
            Log(f"Try to pull manually")
            continue
        Log(f"{dir} Up to date")
        try:
            push_to_origin(None)
        except Exception as e:
            if "git push --set-upstream origin" in str(e):
                branch = str(e).split(" ")[-1]
                if branch:
                    Log(f"Trying to push to {branch} branch")
                    try:
                        push_to_origin(branch)
                    except Exception as e:
                        Log(str(time.ctime()) + " " + dir)
                        handle_exception(e)
                        continue
            else:
                Log(str(time.ctime()) + " " + dir)
                handle_exception(e)
                continue
        Log(f"{dir} Syncronized at {time.ctime()}")
        count += 1

    final_message = f">>>>>{count}/{len(dirs)} syncronized without errors"
    Log(f"\n{final_message}")
    Log("-" * 50 + "\n\n")
    print(final_message)


#--------------------------------------------------------------------------
def config(interval):
    valid_intervals = ["daily", "weekly", "monthly"]
    try:
        # check if number and less than 60
        if int(interval) > 60:
            raise ValueError
    except ValueError:
        if interval not in valid_intervals:
            print(f"{RED}Invalid interval{RESET}")
            sys.exit(1)
        
    try:
        json_content = {
            "interval": interval
        }

        with open(config_file, 'w') as f:
            json.dump(json_content, f)
        print(f"{GREEN}Config set{RESET}")
    except Exception as e:
        print(f"{RED}{e}{RESET}")


def read_interval():
    try:
        with open(config_file, 'r') as f:
            return json.load(f)["interval"]
    except:
        print(f"{RED}File is corrupted{RESET}")
        allow_reset = input(f"{YELLOW}Do you want to reset the file and continue, the interval will be set to daily by default? (y/n){RESET}")
        if allow_reset.lower() == "y":
            with open(config_file, 'w') as f:
                f.write('{"interval": "daily"}')
            print(f"{GREEN}File reset successfully with daily interval{RESET}")
            return "daily"
        else:
            print(f"{RED}Exiting...{RESET}")
            sys.exit(1)


#--------------------------------------------------------------------------
def run_scheduler():

    duration = 60
    interval = read_interval()

    Log(f"\nScheduler started with {interval} interval\n")
    estimated_date = -1
    now = datetime.datetime.now()

    try:
        if int(interval) < 60:
            duration = int(interval)
            schedule.every(int(interval)).minutes.do(run)
            estimated_date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
            Log(f"\nNext run will be at {estimated_date} ⏳\n")
    except:
        pass
    if interval == 'daily':
        schedule.every().day.at("00:00").do(run)
        estimated_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(days=1)
        Log(f"\nNext run will be at {estimated_date} ⏳\n")
    elif interval == 'weekly':
        schedule.every().week.at("00:00").do(run)
        estimated_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(weeks=1)
        Log(f"\nNext run will be at {estimated_date} ⏳\n")
    elif interval == 'monthly':
        schedule.every().month.at("00:00").do(run)
        estimated_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(months=1)
        Log(f"\nNext run will be at {estimated_date} ⏳\n")

    while True:
        schedule.run_pending()
        time.sleep(1)