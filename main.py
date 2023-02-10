from bs4 import BeautifulSoup
import requests
import time
import json


def cooking(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')

exeption = ['/document/cons_doc_LAW_28399/820b4ecd6532a57dd0ff9871cd58c7e0e4542eec/', '/document/cons_doc_LAW_37800/1491c55a429ae57a6cfb2a4075fb018e65a854f6/']
exeption_2 = ['/document/cons_doc_LAW_37800/a6eea06e5adf5cff155294be9f00362a1cd80361/']
soup = cooking('https://www.consultant.ru/popular/')
time.sleep(2)
rules = [x.text for x in soup.find('div', id='content').find_all('h3')]
blockquotes = soup.find_all('blockquote')[:-1]
result = {}
for name_1, block in zip(rules, blockquotes):
    print(name_1)
    result[name_1] = {}
    links = block.find_all('a')
    for link in links:
        name_2 = link.text
        result[name_1][link.text] = {}
        soup = cooking(f'https://www.consultant.ru/{link["href"]}')
        sect = soup.find('div', class_='document-page__toc').find('li')
        while sect:
            if sect.name == 'li': #  Разделы
                name_3 = sect.text
                result[name_1][name_2][name_3] = {}
                print(name_3)
                url = sect.find('a')['href']
                soup = cooking(f"https://www.consultant.ru/{url}")
                if url in exeption:
                    result[name_1][name_2][name_3] = soup.find('div', attrs={'class': 'document-page__content document-page_left-padding'}).text
                else:
                    chapters = soup.find('div', class_='document-page__toc').find_all('li')
                    for chap in chapters:
                        name_4 = chap.text
                        result[name_1][name_2][name_3][name_4] = {}
                        print(name_4)
                        chap_link = chap.find('a')['href']
                        soup = cooking(f"https://www.consultant.ru/{chap_link}")
                        if chap_link in exeption or url in exeption_2:
                            result[name_1][name_2][name_3][name_4] = soup.find('div', attrs={'class': 'document-page__content document-page_left-padding'}).text
                        else:
                            articles = soup.find('div', class_='document-page__toc').find_all('li')
                            for article in articles:
                                name_5 = article.find('a').text
                                result[name_1][name_2][name_3][name_4][name_5] = {}
                                link = article.find('a')['href']
                                print(name_5)
                                soup = cooking(f"https://www.consultant.ru/{link}")
                                text = soup.find('div', class_='document-page__content document-page_left-padding').text
                                result[name_1][name_2][name_3][name_4][name_5] = text
            sect = sect.next_sibling
with open('rules.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
    print('Готово!')

