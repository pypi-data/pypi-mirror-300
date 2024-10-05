import requests
from scrapeanything.database.repository import Repository
from scrapeanything.utils.config import Config
from scrapeanything.utils.api_service import ApiService

class TelegramBot:

    def __init__(self, config: Config) -> None:
        self.TOKEN = config.get(section='NOTIFIERS', key='TELEGRAM_CHATID')
        self.CHAT_ID = config.get(section='NOTIFIERS', key='TELEGRAM_TOKEN')

    def get_chat_id(self) -> str:
        url = f"https://api.telegram.org/bot{self.TOKEN}/getUpdates"
        requests.get(url).json()

    def send_message(self, message: str, receiver: str=None) -> None:
        receiver = receiver if receiver is not None else self.CHAT_ID
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={receiver}&text={message}"
        requests.get(url).json()

    def send_image(self, receiver: str, filename: str, caption: str=None) -> None:
        receiver = receiver if receiver is not None else self.CHAT_ID
        url = f'https://api.telegram.org/bot{self.TOKEN}/sendPhoto'
        files = {'photo': open(f'{filename}.png', 'rb')}
        data = {'chat_id': receiver, 'caption': caption }
        requests.post(url, files=files, data=data)