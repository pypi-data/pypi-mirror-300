import vk_api

class VkAPI:
    def __init__(self, token: str):
        self.vk_session = vk_api.VkApi(token=token)
        self.api = self.vk_session.get_api()

    def send_message(self, user_id: int, message: str):
        self.api.messages.send(user_id=user_id, message=message, random_id=0)