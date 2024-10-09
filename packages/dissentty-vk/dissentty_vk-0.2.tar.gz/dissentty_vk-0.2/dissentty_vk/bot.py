import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dissentty_vk.api import VkAPI

class VkBot:
    def __init__(self, token: str):
        self.api = VkAPI(token)
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.commands = {}

    def listen(self):
        print("Бот запущен и слушает сообщения...")
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.process_message(event)

    def process_message(self, event):
        user_id = event.user_id
        message = event.text.lower()

        if message in self.commands:
            self.commands[message](user_id)
        else:
            self.api.send_message(user_id, "Я не понял вашего сообщения.")

    def add_command(self, command: str, response_function):
        self.commands[command.lower()] = response_function