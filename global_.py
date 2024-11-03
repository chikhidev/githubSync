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
project_root = os.path.join(home, f".__{app_name}")

logs_file = project_root + "/__" + app_name + ".log"
data_file = project_root + "/__dirs.json"
queue_file = project_root + "/__queue.json"
config_file = project_root + "/__config.json"

default_config = '{"interval": "daily", "commit_message": "Syncronized by gitsync"}'