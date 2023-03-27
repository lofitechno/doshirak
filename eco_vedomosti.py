from bs4 import BeautifulSoup
import requests
import pandas as pd

'''В данном ноутбуке парсятся все текущие новости с сайта 
Ведомости-Экология'''

url = 'https://www.vedomosti.ru/ecology'
page = requests.get(url)
print(page.status_code)
filteredNews = []
allNews = []

soup = BeautifulSoup(page.text, 'html.parser')

for link in soup.find('body').find_all('a'):
    print(link.get('href'))

#находим на основной странице ссылки на релизы
release_list = []

for link in soup.find('body').find_all('a'):
    if (link.get('href').startswith('/ecology/release/')):
        print(link.get('href'))
        release_list.append(link.get('href'))

article_list = []

for release in release_list:
    url = 'https://www.vedomosti.ru' + release
    page = requests.get(url)

    # print(page1.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    for link in soup.find_all('a'):
        try:
            if (link.get('href').startswith('/ecology/') and (('release') not in (link.get('href')))):
                print(link.get('href'))
                article_list.append(link.get('href'))
        except:
            pass

#Список для хранения информации        
df_list = []

#Итерация по артиклям
for article in article_list:
    article_data = []
    url = 'https://www.vedomosti.ru' + article
    page = requests.get(url)
    print(page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')

    article_data.append(url)

    # название
    for link in soup.find_all('h1'):
    # print(link.text)
        head = link.text.replace('\n', '').replace('  ', '')
        article_data.append(head)

# аннотация
# for link in soup.find_all('em'):
# print(link.text)
#    article_data.append(link.text)

# дата
    for link in soup.find_all('time'):
    # print(link.text)
        article_data.append(link.text.replace(' /', ''))

# обработка текста статьи
    text_ = ''
    for link in soup.find_all('p'):
    # print(link.text)
        if not link.text.startswith('\n'):
            text_ += (link.text)

    article_data.append(text_)

    df_list.append(article_data)

#Запись списка -> датайфрейм
df = pd.DataFrame(df_list, columns=['Ссылка', 'Заголовок', 'Дата', 'Текст'])
#Датайфрейм - > csv
df.to_csv('data.csv', index=False)