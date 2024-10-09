import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from api import VkAPI

class VkBot:
    def __init__(self, token: str):
        self.api = VkAPI(token)
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk_session)

    def listen(self):
        print("Бот запущен и слушает сообщения...")
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.process_message(event)

    def process_message(self, event):
        user_id = event.user_id
        message = event.text.lower()

        # Здесь можно реализовать логику ответа
        if message == "привет":
            self.api.send_message(user_id, "Привет! Как дела?")
        else:
            self.api.send_message(user_id, "Я не понял вашего сообщения.")