import vk_api
from config import api_token

# Название или короткое имя группы
group_name = 'rhymes'

# Инициализация сессии VK API
vk_session = vk_api.VkApi(token=api_token)
vk = vk_session.get_api()

# Поиск группы
search_results = vk.groups.search(q=group_name)
# print(search_results)

# Вывод результатов (первой найденной группы)
if search_results['count'] > 0:
    for group_info in search_results['items']:    
        # group_info = search_results['items'][0]
        print(f"ID группы '{group_info['name']}': {group_info['id']}")
else:
    print("Группа не найдена.")