from colorama import init
from termcolor import colored

init()

def error(msg):
    print(colored(f'[ERROR] {msg}\n', 'red'))

def warning(msg):
    print(colored(f'[WARNING] {msg}\n', 'yellow'))

def success(msg):
    print(colored(f'[SUCCESS] {msg}\n', 'green'))

def custom(msg, color, tag=''):
    print(colored(f'{tag} {msg}', color))