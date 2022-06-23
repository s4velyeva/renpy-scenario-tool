from enum import Enum
import colorama
from datetime import datetime


colorama.init()

RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.BLUE
YELLOW = colorama.Fore.YELLOW
CYAN = colorama.Fore.CYAN
BOLD = colorama.Style.BRIGHT
DIM = colorama.Style.DIM
RESET = colorama.Style.RESET_ALL

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

class Logger():
    def __init__(self, log_file):
        self.log_file = open(log_file, 'w')
        self.default_level = LogLevel.DEBUG
        self.default_task = 'logger'

    def __call__(self, message, task=None, level=None):
        if task is None:
            task = self.default_task
        if level is None:
            level = self.default_level

        lvl = 'unknown'

        match (level):
            case LogLevel.DEBUG:
                lvl = 'debug'
            case LogLevel.INFO:
                lvl = 'info '
            case LogLevel.WARN:
                lvl = 'warn '
            case LogLevel.ERROR:
                lvl = 'error'

        n = datetime.now()

        print(f'{n.ctime()} - {lvl} - {task} - {message}')
        self.log_file.write(f'{n.ctime()} - {lvl} - {task} - {message}\n')

    def set_task(self, task):
        self.default_task = task

    def set_level(self, level: LogLevel):
        self.default_level = level
