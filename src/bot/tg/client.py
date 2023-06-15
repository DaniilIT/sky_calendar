import requests

from bot.tg.models import GetUpdateResponse, SendMessageResponse


class TgClient:
    def __init__(self, token: str):
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdateResponse:
        url = self.get_url('getUpdates')
        payload = {
            'offset': offset,
            'timeout': timeout
        }
        response = requests.get(url, params=payload)
        return GetUpdateResponse(**response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url('sendMessage')
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.get(url, params=payload)
        return SendMessageResponse(**response.json())
