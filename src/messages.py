from src.bot import *
from src.users import *
from src.admin import *
from src.database import *
from src.keyboards import *
from telethon import events


@bot.on(events.NewMessage)
async def new_message(event):
    try:
        id = event.peer_id.user_id
    except Exception as e:
        id = chat_id
    text, media = event.raw_text, event.media

    logging.info(f'Message|{id}: {text}')

    if '/start' == text:
        txt = 'Вас приветствует бот для знакомств\n'

        if id not in users_list:
            try:
                txt += 'Вам подключено 5 дней бесплатной подписки'
                person = await bot.get_entity(id)
                add_user(id, person.username)
                change_day(id, 5)
            except Exception as e:
                logging.error(str(e))

        if id in admins:
            await bot.send_message(id, txt, buttons=admin_keyboard)
        else:
            await bot.send_message(id, txt, buttons=main_keyboard)

    elif '📄Анкета' == text:
        active = is_user_active(id)
        if not active:
            await bot.send_message(id, 'Начать заполнение анкеты', buttons=Button.inline('✅', 'Form=start'))
        else:
            await bot.send_message(id, '🟢Анкета активна', buttons=[
                [Button.inline('Просмотреть анкету', f'Show={id}')],
                [Button.inline('Удалить анкету', 'Form=close')],
            ])

    elif '💎Оплата' == text:
        time = get_subscription(id)
        if time is None:
            txt = 'Подписка отсутствует'
            await bot.send_message(id, txt, buttons=payment_buttons)
        else:
            txt = f'Последний день подписки: {time}\n'
            await bot.send_message(id, txt, buttons=payment_buttons)

    elif '👁Просмотр анкет' == text:
        active = is_user_active(id)
        if not active:
            txt = 'Необходимо сначала заполнить собственную анкету'
        else:
            if not is_user_girl(id):
                now = datetime.now()
                user_time = get_subscription(id)
                if user_time is None or now < user_time:
                    txt = f'<a href="https://t.me/joinchat/AAAAAFbde26LlkasnMgH9A">Перейти в чат</a>'
                else:
                    txt = 'Необходимо оплатить подписку'
            else:
                txt = 'Данная функция в разработке'
        await bot.send_message(id, txt, parse_mode='HTML')

    elif 'Пропустить' == text and id in form_filling:
        if form_filling[id] == 5:
            txt = 'Действие отменено'
            if id in admins:
                await bot.send_message(id, txt, buttons=admin_keyboard)
            else:
                await bot.send_message(id, txt, buttons=main_keyboard)
            update_user(id, 'latitude', None)
            update_user(id, 'longitude', None)
            form_filling[id] = 6
            await bot.send_message(id, 'Напишите о себе пару слов')

    elif '⚜️Админка' == text:
        set_admin_info(False)
        await bot.send_message(id, 'Выберите меню', buttons=admin_buttons)

    elif 'Завершить' == text:
        companion = get_companion(id)
        if id == get_companion(companion):
            update_user(companion, 'chat_with', 0)
            if companion in admins:
                await bot.send_message(companion, 'Собеседник завершил диалог', buttons=admin_keyboard)
            else:
                await bot.send_message(companion, 'Собеседник завершил диалог', buttons=main_keyboard)

        update_user(id, 'chat_with', 0)
        if id in admins:
            await bot.send_message(id, 'Диалог завершен', buttons=admin_keyboard)
        else:
            await bot.send_message(id, 'Диалог завершен', buttons=main_keyboard)

    elif media is not None:
        if id in form_filling:
            if form_filling[id] == 5:
                update_user(id, 'latitude', media.geo.lat)
                update_user(id, 'longitude', media.geo.long)
                form_filling[id] = 6

                txt = 'Напишите о себе пару слов'
                if id in admins:
                    await bot.send_message(id, txt, buttons=admin_keyboard)
                else:
                    await bot.send_message(id, txt, buttons=main_keyboard)
            elif form_filling[id] == 7:
                await bot.download_media(event.original_update.message, file=f'Photos/{id}.png')
                update_user(id, 'photo', f'Photos/{id}.png')
                update_user(id, 'active', 1)
                del form_filling[id]
                await bot.send_message(id, 'Заполнение анкеты завершено')
                if is_user_girl(id):
                    await bot.send_file(
                        chat_id,
                        file=get_photo(id),
                        parse_mode='HTML',
                        caption=dict_to_str(get_user(id)),
                        buttons=Button.inline('Написать', f'Dialog={id}')
                    )

    elif id in admins and get_admin_info():
        try:
            user_id = int(text)
            person = await bot.get_entity(user_id)
            await bot.send_message(id, 'Посмотреть профиль пользователя?', buttons=[
                Button.inline('✅', f'Info={user_id}'), Button.inline('❌', '⚜️Админка')
            ])
        except ValueError:
            await bot.send_message(id, 'Неверный 🆔', buttons=Button.inline('❌Отмена', '⚜️Админка'))

    elif id in form_filling:
        stage = form_filling[id]
        if stage == 1:           # ИМЯ и ФАМИЛИЯ
            try:
                f_name, l_name = text.split()
                update_user(id, 'f_name', f_name)
                update_user(id, 'l_name', l_name)
                form_filling[id] = 2
                await bot.send_message(id, 'Введите ваш возраст')
            except ValueError:
                await bot.send_message(id, 'Неверный формат данных')
        elif stage == 2:         # ВОЗРАСТ
            try:
                age = int(text)
                if not(10 <= age <= 99):
                    raise ValueError
                update_user(id, 'age', age)
                form_filling[id] = 3
                await bot.send_message(id, 'Выберите ваш пол', buttons=choose_sex)
            except ValueError:
                await bot.send_message(id, 'Неверный формат данных')
        elif stage == 4:         # ГОРОД
            try:
                update_user(id, 'city', text)
                form_filling[id] = 5
                await bot.send_message(id, 'Поделиться Геопозицией', buttons=geolocation_buttons)
            except Exception as e:
                logging.error(str(e))
        elif stage == 6:         # ЛИЧНАЯ ИНФОРМАЦИЯ
            update_user(id, 'about', text)
            form_filling[id] = 7
            await bot.send_message(id, 'Отправьте фотографию профиля')

    else:
        companion = get_companion(id)
        if companion != 0:
            if id == get_companion(companion):
                await bot.send_message(companion, text)
            else:
                await bot.send_message(id, 'Собеседник ещё не принял запрос')

        # if id in admins:
        #     await bot.send_message(chat_id, text)
