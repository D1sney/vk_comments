import requests
from bs4 import BeautifulSoup
import pymysql
import json

wall_url = 'https://vk.com/dfl_strogino'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
  }

def parse_wall(wall_url):
    # Отправляем запрос на веб-сайт
    response = requests.get(wall_url, headers = headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'lxml') # html.parser

        soup2 = soup.find('div', class_ = 'wall_posts own mark_top')

        # Находим список комментариев
        comments = soup2.find_all('div', class_ = 'reply_wrap _reply_content _post_content clear_fix', limit = 100)

        for comment in comments:
            text = comment.find('div', class_ = 'wall_reply_text').text.strip()
            author_link = comment.find('a', class_ = 'author author_highlighted').get('href')
            author_name = comment.find('a', class_ = 'author author_highlighted').text.strip()
            
            print(author_name, author_link, text)
    else:
        print(f"Ошибка при запросе. Статус код: {response.status_code}")

parse_wall(wall_url)