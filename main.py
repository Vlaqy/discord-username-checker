import datetime
from random import sample as rand_sample
from string import ascii_letters, digits
from requests import post as req_post
from time import sleep
from colorama import Fore, init
import colorama
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Discordo :3")

BASE_URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

REQUEST_HEADERS = {
    "Content-Type": "Application/json",
    "Orgin": "https://discord.com/",
    "Authorization": "Token-Here"
}

checked_usernames = set()

def generate_random_username(length: int) -> str:
    characters = ascii_letters + digits
    return ''.join(rand_sample(characters, length))

def check_username(user):
    if 2 > len(user) < 33:
        print(f"{Fore.YELLOW}[{Fore.WHITE}{get_timestamp()}{Fore.YELLOW}] [Error] Username must be 2-32 Characters{Fore.RESET}")
        return
        
    if user in checked_usernames:
        print(f"{Fore.CYAN}[{Fore.WHITE}{get_timestamp()}{Fore.CYAN}] {user} already checked{Fore.RESET}")
        return

    data = {
        "username": user
    }
    check = req_post(BASE_URL, headers=REQUEST_HEADERS, json=data)
    
    try:
        if check.json()["taken"] is not True:
            print(f"{Fore.GREEN}[{Fore.WHITE}{get_timestamp()}{Fore.GREEN}] {user} is available{Fore.RESET}")
            save_valid_username(user)
        else:
            print(f"{Fore.RED}[{Fore.WHITE}{get_timestamp()}{Fore.RED}] {user} is not available{Fore.RESET}")
    except KeyError:
        if check.status_code == 403 or check.status_code == 401:
            print(f"{Fore.YELLOW}[{Fore.WHITE}{get_timestamp()}{Fore.YELLOW}] [Error] Request denied. Check your Discord token or limit your requests{Fore.RESET}")
            return False

    checked_usernames.add(user)

def get_timestamp() -> str:
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    return current_time

def main_menu() -> int:
    init()
    user_length = int(input(f"{Fore.BLUE}Amount of characters >{Fore.RESET} "))
    return user_length

def save_valid_username(username: str):
    with open("valid.txt", "a") as file:
        file.write(username + "\n")

if __name__ == "__main__":
    username_length = main_menu()

    while True:
        user = generate_random_username(username_length)
        check_username(user)
        with open("dnt.txt", "a") as file:
            file.write(user + "\n")
        sleep(1.3)
