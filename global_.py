import os
import json
import sys
import subprocess
import time
import datetime
import schedule

app_name = "gitsync"
system = os.name
SYS = "LINUX" if system == 'posix' else "WINDOWS"
data_file = "__dirs.json"
user = os.getlogin()
logs_file = f"/home/{user}/{app_name}.log" if SYS == "LINUX" else f"C:\\Users\\{user}\\{app_name}.log"
queue_file = "__queue"
config_file = "__config.json"