import vk_api
from config import api_token

# ID группы, в которой вы хотите получить комментарии
group_id = '28905875'
# all_comments = []

vk_session = vk_api.VkApi(token=api_token)
vk = vk_session.get_api()

# Получение информации о последнем посте на стене группы
def get_all_comments(my_offset, my_count):
    try:
        wall = vk.wall.get(owner_id=f"-{group_id}",offset=my_offset, count=my_count) # Параметр offset в запросах к VK API указывает, сколько элементов (в данном случае, комментариев) следует пропустить перед началом загрузки данных. Он представляет собой смещение в результате запроса.
        if wall and 'items' in wall:
            for last_post in wall['items']: 
                post_id = last_post['id']

                # Функция для получения комментариев и ответов к комментариям (рекурсивно)
                def get_comments(parent_id, level=0):
                    comments = vk.wall.getComments(owner_id=f"-{group_id}", post_id=post_id, comment_id=parent_id, count=100) # у комментариев по ключу thread содержится количество ответов на комментарий, но у комментариев которые являются ответами на другие комментарии нет этого ключа, о в отличии от обычнах комментариев в них по ключу parents_stack находится id комментария на который эти комментарии ссылаются как ответ ( у обычных комментариев по ключу parents_stack находится пустой список)
                    # all_comments.append(comments)
                    if 'items' in comments:
                        for comment in comments['items']:
                            comment_id = comment['id']
                            user_id = comment['from_id']
                            print('  ' * level + f'Пользователь {user_id}:')

                            # Получаем текст комментария
                            comment_text = comment['text']
                            print('  ' * level + f'Комментарий: {comment_text}')

                            # Рекурсивно получаем ответы на комментарий
                            get_comments(parent_id=comment_id, level=level + 1)

                print(f"Комментарии и ответы под постом (ID {post_id}):")
                # Начинаем с корневых комментариев (parent_id = 0)
                get_comments(parent_id=0)
        else:
            print("Постов нет в указанной группе.")
    except vk_api.exceptions.ApiError as e:
        print(f"Произошла ошибка при запросе к VK API: {e}")

a = 0
b = 50
for i in range(10):
    get_all_comments(a,b)
    a +=50