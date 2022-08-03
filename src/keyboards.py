from telethon.tl.types import *
from telethon.tl.custom import *

main_keyboard = [
    [Button.text('📄Анкета', resize=True), Button.text('💎Оплата', resize=True)],
    [Button.text('👁Просмотр анкет', resize=True)],
]

admin_keyboard = [
    [Button.text('📄Анкета', resize=True), Button.text('💎Оплата', resize=True)],
    [Button.text('👁Просмотр анкет', resize=True)],
    [Button.text('⚜️Админка')],
]

dialog_keyboard = [
    [Button.text('Завершить', resize=True)],
]

admin_buttons = [
    [Button.inline('Список пользователей', 'List')],
    [Button.inline('Информация о пользователе', 'Info')],
]

choose_sex = [
    Button.inline('Мужской', 'Sex=0'), Button.inline('Женский', 'Sex=1')
]

geolocation_buttons = [
    Button.request_location('Поделиться геопозицией', resize=True), Button.text('Пропустить', resize=True)
]

payment_buttons = [
    Button.inline('Оплатить 10💶 за 10 дней', 'Pay=10')
]


