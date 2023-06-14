import datetime
from random import sample as rand_sample
from string import ascii_lowercase
from requests import post as req_post
from time import sleep
import colorama
from colorama import Fore, Style
import ctypes

# Set console title
ctypes.windll.kernel32.SetConsoleTitleW("Made by Vlaq")

BASE_URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://discord.com/",
    "Authorization": "MzA4MzA1MDk5NzQxMjAwMzg0.Gzyaln.W2Ck8HY072eLVb1q-bnj8nNk1PYJ6fh6c__m28"
}

request_number = 0
checked_usernames = set()

def generate_random_username(length: int) -> str:
    return ''.join(rand_sample(ascii_lowercase, length))

def check_username(user: str):
    global request_number
    request_number += 1

    if not (1 <= len(user) <= 32):
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
        if check.json().get("taken") is not True:
            # Double-check if the username is really available
            sleep(1)  # Wait for 1 second before rechecking
            recheck = req_post(BASE_URL, headers=REQUEST_HEADERS, json=data)

            if recheck.json().get("taken") is not True:
                print(f"{Fore.GREEN}[{Fore.WHITE}{get_timestamp()}{Fore.GREEN}] {user} is available{Fore.RESET}")
                save_valid_username(user)
            else:
                print(f"{Fore.YELLOW}[{Fore.WHITE}{get_timestamp()}{Fore.YELLOW}] {user} is not available (Double-checked){Fore.RESET}")
        else:
            print(f"{Fore.RED}[{Fore.WHITE}{get_timestamp()}{Fore.RED}] {user} is not available{Fore.RESET}")
    except KeyError:
        if check.status_code == 403 or check.status_code == 401:
            print(f"{Fore.YELLOW}[{Fore.WHITE}{get_timestamp()}{Fore.YELLOW}] [Error]{Fore.RESET}")
            return False

    checked_usernames.add(user)

def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")

def main_menu() -> int:
    flag = False
    while not flag:
        try:
            user_length = int(input("Amount of characters >"))
            flag = True
        except ValueError:
            print(f"{Fore.YELLOW}[{Fore.WHITE}{get_timestamp()}{Fore.YELLOW}] [Error] Enter a correct value.{Fore.RESET}")
    return user_length

def save_valid_username(username: str):
    with open("valid.txt", "a") as file:
        file.write(username + "\n")

if __name__ == "__main__":
    colorama.init()
    username_letters = main_menu()

    while True:
        user = generate_random_username(username_letters)
        check_username(user)
        with open("dnt.txt", "a") as file:
            file.write(user + "\n")
        sleep(1)
