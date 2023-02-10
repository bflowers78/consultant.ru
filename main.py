from bs4 import BeautifulSoup
import requests
import time
import json


def cooking(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


exeption = [
    '/document/cons_doc_LAW_371232/',
    '/document/cons_doc_LAW_315739/',
    '/document/cons_doc_LAW_32451/94b17bafb57578dce2b04c8941777f7b2b7922cb/']
soup = cooking('https://www.consultant.ru/popular/')
time.sleep(2)
rules = [x.text for x in soup.find('div', id='content').find_all('h3')][1]
blockquotes = soup.find_all('blockquote')[:-1][1]
result = {}
'''for name_1, block in zip(rules, blockquotes):
    print(name_1, '  ***')
    result[name_1] = {}
    links = block.find_all('a')'''
name_1 = rules
print(name_1, '  ***')
result[name_1] = {}
links = blockquotes.find_all('a')
for link in [links[13], links[14]]:
    if link in exeption:
        continue
    name_2 = link.text
    print(name_2)
    result[name_1][link.text] = {}
    soup = cooking(f'https://www.consultant.ru/{link["href"]}')
    sect = soup.find('div', class_='document-page__toc').find_all('li')
    print(sect)
    while sect:
        if sect.name == 'li':
            name_3 = sect.text
            print(name_3, '------------------------------------------------------')
            result[name_1][name_2][name_3] = {}
            try:
                link_2 = sect.find('a')['href']
                soup = cooking(f"https://www.consultant.ru/{link_2}")
                chapters = soup.find('div', class_='document-page__toc').find_all('li')
                for chap in chapters:
                    name_4 = chap.text
                    print(name_4)
                    result[name_1][name_2][name_3][name_4] = {}
                    try:
                        link_3 = chap.find('a')['href']
                        soup = cooking(f"https://www.consultant.ru/{link_3}")
                        articles = soup.find('div', class_='document-page__toc').find_all('li')
                        for article in articles:
                            name_5 = article.find('a').text
                            print(name_5)
                            result[name_1][name_2][name_3][name_4][name_5] = {}
                            try:
                                link_4 = article.find('a')['href']
                                soup = cooking(f"https://www.consultant.ru/{link_4}")
                                articles_2 = soup.find('div', class_='document-page__toc').find_all('li')
                                for article_2 in articles_2:
                                    name_6 = article_2.find('a').text
                                    print(name_6)
                                    result[name_1][name_2][name_3][name_4][name_5][name_6] = {}
                                    soup = cooking(f"https://www.consultant.ru/{article_2.find('a')['href']}")
                                    result[name_1][name_2][name_3][name_4][name_5][name_6] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
                            except Exception as err:
                                print(err)
                                result[name_1][name_2][name_3][name_4][name_5] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
                    except Exception as err:
                        print(err)
                        result[name_1][name_2][name_3][name_4] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
            except Exception as err:
                print(err)
                result[name_1][name_2][name_3] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
        sect = sect.next_sibling
    with open('rules.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
        print('Готово!')

