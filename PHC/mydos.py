import threading
import requests
import time


# Функция, которая отправляет POST-запрос
def send_post_request():
    url = "http://example.com/your_endpoint"  # Замените на ваш URL
    data = {"key": "value"}  # Данные, которые вы хотите отправить в POST-запросе
    headers = {
        "Content-Type": "application/json"
    }  # Установите заголовки по вашему выбору

    while True:
        response = requests.post(url, json=data, headers=headers)
        print(response.status_code)  # Выводим статус ответа для проверки
        time.sleep(1)  # Пауза в 1 секунду между запросами


# Создаем потоки для отправки POST-запросов
threads = []
for _ in range(1000):  # Создаем 1000 потоков для достижения 1000 запросов в секунду
    thread = threading.Thread(target=send_post_request)
    threads.append(thread)
    thread.start()

# Ждем завершения всех потоков
for thread in threads:
    thread.join()
