import os
import json
import sys
import subprocess
import time
import datetime
import schedule

app_name = "gitsync"
system = os.name
SYS = "LINUX" if system == 'posix' else "OTHER"
user = os.getlogin()
home = os.path.expanduser("~")
project_root = home + "/." + app_name
logs_file = project_root + "/" + app_name + ".log"
data_file = project_root + "/dirs.json"
queue_file = project_root + "/queue.json"
config_file = project_root + "/config.json"
enable_file = project_root + "/enable"

default_config = '{"interval": "daily", "commit_message": "Syncronized by gitsync"}'

gitsync_branch = "gitsync_"