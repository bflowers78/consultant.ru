from bs4 import BeautifulSoup
import requests
import time
import json


def cooking(url):
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


soup = cooking('https://www.consultant.ru/popular/')
time.sleep(2)
rules = [x.text for x in soup.find('div', id='content').find_all('h3')]
blockquotes = soup.find_all('blockquote')[:-1]
result = {}
for name_1, block in zip(rules, blockquotes):
    print(name_1, '  ***')
    result[name_1] = {}
    links = block.find_all('a')
    for link in links:
        name_2 = link.text
        print(name_2, '|2')
        result[name_1][name_2] = {}
        soup = cooking(f'https://www.consultant.ru/{link["href"]}')
        section_1 = soup.find('div', class_='document-page__toc').find('li')
        show = [x.text for x in section_1]
        while section_1:
            if section_1.name == 'li':
                name_3 = section_1.find('a').text
                print(name_3, '|3------------------------------------------------------')
                result[name_1][name_2][name_3] = {}
                try:
                    link_2 = section_1.find('a')['href']
                    soup = cooking(f"https://www.consultant.ru/{link_2}")
                    section_2 = soup.find('div', class_='document-page__toc').find_all('li')
                    for el2 in section_2:
                        name_4 = el2.find('a').text
                        print(name_4, '|4')
                        result[name_1][name_2][name_3][name_4] = {}
                        try:
                            link_3 = el2.find('a')['href']
                            soup = cooking(f"https://www.consultant.ru/{link_3}")
                            section_3 = soup.find('div', class_='document-page__toc').find_all('li')
                            for el3 in section_3:
                                name_5 = el3.find('a').text
                                print(name_5, '|5')
                                result[name_1][name_2][name_3][name_4][name_5] = {}
                                try:
                                    link_4 = el3.find('a')['href']
                                    soup = cooking(f"https://www.consultant.ru/{link_4}")
                                    section_4 = soup.find('div', class_='document-page__toc').find_all('li')
                                    for el4 in section_4:
                                        name_6 = el4.find('a').text
                                        print(name_6, '|6')
                                        result[name_1][name_2][name_3][name_4][name_5][name_6] = {}
                                        soup = cooking(f"https://www.consultant.ru/{el4.find('a')['href']}")
                                        result[name_1][name_2][name_3][name_4][name_5][name_6] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
                                except Exception as err:
                                    print(err)
                                    try:
                                        result[name_1][name_2][name_3][name_4][name_5] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
                                    except Exception as err:
                                        print(f'{name_5} больше не актуальна')
                                        result[name_1][name_2][name_3][name_4][name_5] = soup.find('div', class_='document__style doc-style').text
                        except Exception as err:
                            print(err)
                            try:
                                result[name_1][name_2][name_3][name_4] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
                            except Exception as err:
                                print(f'{name_4} больше не актуальна')
                                result[name_1][name_2][name_3][name_4] = soup.find('div', class_='document__style doc-style').text
                except Exception as err:
                    print(err)
                    try:
                        result[name_1][name_2][name_3] = soup.find('div', class_='document-page__content document-page_left-padding').text.split('\n\n')[-2]
                    except Exception as err:
                        print(f'{name_3} больше не актуальна')
                        result[name_1][name_2][name_3] = soup.find('div', class_='document__style doc-style').text
            section_1 = section_1.next_sibling
    with open(f'{name_1}.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
        print('Готово!')

