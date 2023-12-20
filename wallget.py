import vk_api
import json
from config import api_token

# ID группы, в которой вы хотите получить комментарии
group_id = '212056973'

# функция отображения словаря
def view(dicl, level):
    if level<5:
        for i in dicl:
            print(f'level {level} - {i}')           
            if type(dicl) == dict:
                if type(dicl[i]) != str and type(dicl[i]) != int and type(dicl[i]) != bool:
                    view(dicl[i], level + 1)
            elif type(dicl) == list:
                if type(i) != str and type(i) != int and type(i) != bool:
                    view(i, level + 1)
            else:
                print(f'{type(i)} не попало под условия')

        # print(f'{i} - not itterable')
        

# Инициализация сессии VK API
vk_session = vk_api.VkApi(token=api_token)
vk = vk_session.get_api()


# Получение информации о последнем посте на стене группы
try:
    wall = vk.wall.get(owner_id=f"-{group_id}", count=10)
    if wall and 'items' in wall:
        # view(wall, 1)
        # print(wall)
        last_post = wall['items']
        # print(wall['items'][0]['id'])
        for last_post in wall['items']:    
            post_id = last_post['id']

            # Получение комментариев к последнему посту
            comments = vk.wall.getComments(owner_id=f"-{group_id}", post_id=post_id)

            # Вывод комментариев
            if 'items' in comments:
                print(f"Комментарии под последним постом (ID {post_id}):")
                for comment in comments['items']:
                    comment_text = comment['text']
                    user_id = comment['from_id']
                    print(f'Пользователь {user_id}: {comment_text}')
                    # print(comment)
                    if 'thread' in comment and 'items' in comment['thread']:
                        reply = vk.wall.getComments(owner_id=f"-{group_id}", post_id=post_id, count=100, thread_items=1, comment_id=comment['id'])
                        # print(reply)
                        reply_text = reply['items'][0]['text']
                        reply_id = reply['items'][0]['from_id']
                        print(f'Пользователь {reply_id}: {reply_text}')
            else:
                print("Комментариев нет.")
    else:
        print("Постов нет в указанной группе.")
except vk_api.exceptions.ApiError as e:
    print(f"Произошла ошибка при запросе к VK API: {e}")


# Завершение сессии VK API
# vk_session.close()



