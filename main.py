from bs4 import BeautifulSoup
import requests
import json
import time
import smtplib
from email.mime.text import MIMEText


def cooking(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


def send_email(message):
    try:
        sender = "parserconsultanta@gmail.com"
        password = "kxdtifqdrrilbyia"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Парсер"
        server.sendmail(sender, 'consultant-Jur@yandex.ru', msg.as_string())
        print('Сообщение отправлено')
    except Exception as err:
        print(err)


def findDiff(d1, d2, path=""):
    global res_path
    global change_links
    global new_key
    for k in d2.keys():
        if k not in d1.keys():
            new_key.append([f'Была добавлена {k}', path.split('\\')[1]])
    for k in d1.keys():
        if k not in d2.keys():
            new_key.append([f'Была удалена {k}', path.split('\\')[1]])
        else:
            if type(d1[k]) is dict:
                path = k if not path else path + "\\" + k
                findDiff(d1[k], d2[k], path)
            else:
                if d1[k] != d2[k]:
                    print(path, ":")
                    print(" - ", k, " : ", d1[k][0])
                    print(" + ", k, " : ", d2[k][0])
                    adress = [path.split('\\')[1], k]
                    if adress not in res_path:
                        res_path.append(adress)
                    if d2[k][1] not in change_links:
                        change_links.append(d2[k][1])


soup = cooking('https://www.consultant.ru/popular/')
time.sleep(2)
rules = [x.text for x in soup.find('div', id='content').find_all('h3')]
blockquotes = soup.find_all('blockquote')[:-1]
result_new = {}
for name_1, block in zip(rules, blockquotes):
    print(name_1)
    result_new[name_1] = {}
    links = block.find_all('a')
    if block == blockquotes[2]:
        links = links[:-3]
    for link in links:
        name_2 = link.text
        print(name_2)
        result_new[name_1][name_2] = {}
        soup = cooking(f'https://www.consultant.ru/{link["href"]}')
        try:
            section_1 = soup.find('div', class_='document-page__toc').find('li')
            show = [x.text for x in section_1]
            while section_1:
                if section_1.name == 'li':
                    name_3 = section_1.find('a').text
                    print(name_3)
                    result_new[name_1][name_2][name_3] = {}
                    try:
                        link_2 = section_1.find('a')['href']
                        soup = cooking(f"https://www.consultant.ru/{link_2}")
                        section_2 = soup.find('div', class_='document-page__toc').find_all('li')
                        for el2 in section_2:
                            name_4 = el2.find('a').text
                            print(name_4)
                            result_new[name_1][name_2][name_3][name_4] = {}
                            try:
                                link_3 = el2.find('a')['href']
                                soup = cooking(f"https://www.consultant.ru/{link_3}")
                                section_3 = soup.find('div', class_='document-page__toc').find_all('li')
                                for el3 in section_3:
                                    name_5 = el3.find('a').text
                                    print(name_5)
                                    result_new[name_1][name_2][name_3][name_4][name_5] = {}
                                    try:
                                        link_4 = el3.find('a')['href']
                                        soup = cooking(f"https://www.consultant.ru/{link_4}")
                                        section_4 = soup.find('div', class_='document-page__toc').find_all('li')
                                        for el4 in section_4:
                                            name_6 = el4.find('a').text
                                            print(name_6)
                                            result_new[name_1][name_2][name_3][name_4][name_5][name_6] = {}
                                            soup = cooking(f"https://www.consultant.ru/{el4.find('a')['href']}")
                                            result_new[name_1][name_2][name_3][name_4][name_5][name_6] = [soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2], f"https://www.consultant.ru/{el4.find('a')['href']}"]
                                    except Exception as err:
                                        try:
                                            result_new[name_1][name_2][name_3][name_4][name_5] = [soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2], f"https://www.consultant.ru/{link_4}"]
                                        except Exception as err:
                                            print(f'{name_5} больше не актуальна')
                                            result_new[name_1][name_2][name_3][name_4][name_5] = [soup.find('div', class_='document__style doc-style').text, f"https://www.consultant.ru/{link_4}"]
                            except Exception as err:
                                try:
                                    result_new[name_1][name_2][name_3][name_4] = [soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2], f"https://www.consultant.ru/{link_3}"]
                                except Exception as err:
                                    print(f'{name_4} больше не актуальна')
                                    result_new[name_1][name_2][name_3][name_4] = [soup.find('div', class_='document__style doc-style').text, f"https://www.consultant.ru/{link_3}"]
                    except Exception as err:
                        try:
                            result_new[name_1][name_2][name_3] = [soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2], f"https://www.consultant.ru/{link_2}"]
                        except Exception as err:
                            print(f'{name_3} больше не актуальна')
                            result_new[name_1][name_2][name_3] = [soup.find('div', class_='document__style doc-style').text, f"https://www.consultant.ru/{link_2}"]
                section_1 = section_1.next_sibling
        except Exception as err:
            with open('result.json', 'r', encoding='utf-8') as file:
                gag_dict = json.load(file)
            result_new[name_1][name_2] = gag_dict[name_1][name_2]
            print(err)
print('Чтение старого файла')
with open('result.json', 'r', encoding='utf-8') as file:
    result_old = json.load(file)
res_path = []
change_links = []
new_key = []
findDiff(result_old, result_new)

if len(res_path) != 0 or len(new_key) != 0:
    message = 'На сайте https://www.consultant.ru/popular/ обнаружены изменения: \n'
    for res, link in zip(res_path, change_links):
        message += f'{res[0]}, {res[1]}: \n{link}\n'
    message += '\n'
    for nk in new_key:
        message += f'{nk[0]} | {nk[1]}\n'
    send_email(message)
    try:
        with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(result_new, file, indent=4, ensure_ascii=False)
            print('Данные в словаре обновлены')
    except Exception as err:
        send_email('Не удалось сохранить файл result.json')
else:
    send_email('Изменения не обнаружены')
