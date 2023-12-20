import requests
import time
from config import api_token

# ID паблика
group_id = '212056973'

# Получение постов из паблика
def get_posts(group_id, api_token):
    posts = []
    offset = 0
    count = 100  # Максимальное значение для count
    while True:
        time.sleep(0.2)
        response = requests.get(
            f'https://api.vk.com/method/wall.get',
            params={'owner_id': f'-{group_id}', 'count': count, 'offset': offset, 'access_token': api_token, 'v': 5.92}
        )
        data = response.json()
        if 'response' in data:
            items = data['response']['items']
            if not items:
                break
            posts.extend(items)
            offset += count
        else:
            print(f"Произошла ошибка при запросе к VK API: {data.get('error', '')}")
            break
    return posts

# Получение комментариев к посту
def get_comments(post, api_token):
    post_id = post['id']
    comments = []
    offset = 0
    count = 100
    while True:
        time.sleep(0.2)
        response = requests.get(
            f'https://api.vk.com/method/wall.getComments',
            params={'owner_id': post['owner_id'], 'post_id': post_id, 'count': count, 'offset': offset, 'access_token': api_token, 'v': 5.92}
        )
        data = response.json()
        if 'response' in data:
            items = data['response']['items']
            if not items:
                break
            comments.extend(items)
            offset += count
        else:
            print(f"Произошла ошибка при запросе к VK API: {data.get('error', '')}")
            break
    return comments

# Получение ответов на комментарии
def get_comment_replies(comment, api_token):
    comment_id = comment['id']
    replies = []
    offset = 0
    count = 100
    while True:
        time.sleep(0.2)
        response = requests.get(
            f'https://api.vk.com/method/wall.getComments',
            params={'owner_id': comment['owner_id'], 'post_id': comment['post_id'], 'comment_id': comment_id, 'count': count, 'offset': offset, 'access_token': api_token, 'v': 5.92}
        )
        data = response.json()
        if 'response' in data:
            items = data['response']['items']
            if not items:
                break
            replies.extend(items)
            offset += count
        else:
            print(f"Произошла ошибка при запросе к VK API: {data.get('error', '')}")
            break
    return replies

# Получаем посты из паблика
posts = get_posts(group_id, api_token)

# Проходимся по каждому посту и получаем комментарии
for post in posts:
    print(f"Пост ID: {post['id']}, Текст: {post['text']}")
    comments = get_comments(post, api_token)
    for comment in comments:
        print(f"Комментарий ID: {comment['id']}, Текст: {comment['text']}")
        replies = get_comment_replies(comment, api_token)
        for reply in replies:
            print(f"Ответ ID: {reply['id']}, Текст: {reply['text']}")
