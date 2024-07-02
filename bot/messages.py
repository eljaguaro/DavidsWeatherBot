import abc

import telegram as tg
import telegram.ext as tg_ext
import requests


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def help(self) -> str:
        raise NotImplemented


    @abc.abstractmethod
    def weather(self, text: str) -> str:
        raise NotImplemented


class RegularUser(BaseMessages):

    def start(self):
        return 'Привет!'

    def help(self):
        return 'Вам необходимо приобрести премиум-подписку для связи с поддержкой'

    def weather(self, text: str):
        return 'Вам необходимо приобрести премиум-подписку для запроса погоды'


class PremiumUser(RegularUser):

    def help(self):
        return 'Наш менеджер скоро свяжется с Вами!'

    def weather(self, city: str):
        if city == 'Даня Чанба':
            return 'в этом данчоусе уровень нефорства составляет 100%'
        APIkey = 'c5b958b340553dc18809850bcb581bd3'
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIkey}&units=metric').json()
        if 'main' not in res:
            return 'Извините, мы про такой город слышим впервые'
        temp = res['main']['temp']
        return f'В этом городе сейчас температура воздуха составляет {temp}°C'



def get_messages(user: tg.User) -> BaseMessages:
    if user.is_premium:
        return PremiumUser()
    return RegularUser()
