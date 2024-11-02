import os
import json
import sys

app_name = "gitsync"
system = os.name
SYS = "LINUX" if system == 'posix' else "WINDOWS"
data_file = "__dirs.json"
user = os.getlogin()