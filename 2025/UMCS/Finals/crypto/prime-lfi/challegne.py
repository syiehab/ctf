from nprime import miller_rabin
from base64 import b64decode
import random

def ascii_art():
    banner = """
┌───────────────────────────────────────────┬─────────────────────────┐
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           │                         │
│                                           ├─────┬───┬───────────────┤
│                                           │     │   │               │
│                                           │     ├─┬─┤               │
│                                           ├─────┴─┴─┤               │
│                                           │         │               │
│                                           │         │               │
│                                           │         │               │
│                                           │         │               │
└───────────────────────────────────────────┴─────────┴───────────────┘
    """
    return banner

def menu(n):
    print("[+] Please select anything you want from me.")
    print("[1] Get server.py\n[2] Get flag format\n[3] Flag checker\n[4] Exit")
    try:
        option = int(input("[>] "))
        if option == 1:
            print(miller_test())
        elif option == 2:
            print(f"[+] Since you ask for it, I mean... sure\n[+] {n[:5].decode()}}}\n")
        elif option == 3:
            flag = input("[>] Let me check whether you have my flag already\n[>] FLAG: ")
            print(flag_checker(flag))
            exit()
        elif option == 4:
            print("[-] Exit program...")
            exit()
        else:
            print("[-] Sorry, I don't accept nonsense.")
            exit()
    except Exception:
        print("[-] Sorry, I don't accept nonsense.")
        exit()

def miller_test():
    print("[+] You can't get the file unless you send me a good PRIME password.")
    try:
        p = int(input("[>] "))
        a = int(input(f"[+] Enter BASE 'captcha'. E.g. {random.getrandbits(32)}\n[>] "))
        if p < 1 or a < 1:
            return "[-] Sorry, I don't accept nonsense. Positive integers.\n"
        if p.bit_length() < 400:
            return "[-] Who's password will use that short?\n"
        if p.bit_length() > 500:
            return "[-] I don't accept numbers that big.\n"
        if not miller_rabin(p):
            return "[-] Sir, I am pretty sure prime number is easy to understand?\n"
        if p < a:
            return "[-] What are you trying to do?\n"
        x = pow(a, p-1, p)
        print(f"[+] Through fermat's little theorem...\n[+] Nice prime! Here's {x} bit of file contents: \n")
        with open(__file__, 'r') as f:
            content = f.read()
        return content[:x]
    except Exception as e:
        return f"[-] Sorry, I don't accept nonsense.\n"

def flag_checker(n):
    global FLAG
    if n == b64decode(FLAG).decode():
        return "\033[32;1m[+] ACCESS GRANTED!\n[+] Please proceed to submit the flag.\033[0m\n[+] Or you done it already hehe."
    else:
        return "\033[31;1m[-] Boo!\033[0m"

FLAG = "VU1DU3tTb21lX3ByaW1lc19hcmVfcHNldWRvcHJpbWVzX3NuZWFrc19hbmRfYnJlYWtzX215X21pbGxlcn0="

def main():
    print(ascii_art())
    print("[+] Welcome to Fibonacci Windows! Any password here MUST be a prime number.")
    while True:
        try:
            menu(b64decode(FLAG))
        except KeyboardInterrupt:
            print("\n[-] Exit program...")
            exit()

if __name__=="__main__":
    main()