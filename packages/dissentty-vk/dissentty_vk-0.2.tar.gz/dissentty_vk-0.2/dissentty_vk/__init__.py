# my_vk_bot/__init__.py

__version__ = '0.2'
__author__ = 'Ваше Имя'
__license__ = 'MIT'

# Импорт ключевых компонентов библиотеки
from dissentty_vk.api import VkAPI
from dissentty_vk.bot import VkBot

# Опциональная инициализация при импорте библиотеки
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Библиотека {__name__} версии {__version__} инициализирована")