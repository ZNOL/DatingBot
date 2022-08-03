from src.bot import *
from src.users import *
from src.admin import *
from src.paypal import *
from src.database import *
from src.keyboards import *
from telethon import events
from datetime import datetime


@bot.on(events.callbackquery.CallbackQuery())
async def new_button(event):
    try:
        id = event.original_update.user_id
    except Exception as e:
        id = chat_id
    command = event.original_update.data.decode('utf-8')

    logging.info(f'Command|{id}: {command}')

    if '⚜️Админка' == command:
        set_admin_info(False)
        await bot.send_message(id, 'Выберите меню', buttons=admin_buttons)

    elif 'List' == command:
        await event.delete()
        request = get_users()
        for i in range(0, len(request), 20):
            tmp = request[i: i + 20]
            txt = ''
            for j in range(len(tmp)):
                txt += f'🆔: `{tmp[j]["user_id"]}`\n'
                if tmp[j]["username"] is not None:
                    txt += f'USERNAME: @{tmp[j]["username"]}\n'

                if tmp[j]["active"]:
                    txt += '🟢Анкета активна\n'
                else:
                    txt += '🔴Анкета отсутвует\n'

                if tmp[j]["subscription"] is not None:
                    txt += f'Дата окончания подписки: {tmp[j]["subscription"]}\n'
                else:
                    txt += 'Подписка отсутвует\n'

                if tmp[j]["is_fake"]:
                    txt += '♦️Фейк\n'
                else:
                    txt += '🔷Не фейк\n'

                if tmp[j]["chat_with"] == 0:
                    txt += 'Не вступил(а) в чат\n'
                else:
                    txt += f'В чате с {tmp[j]["chat_with"]}\n'

                txt += '\n\n'
            await bot.send_message(id, txt)
        await bot.send_message(id, 'Узнать о конкретном пользователе?',
                               buttons=[Button.inline('Ввести 🆔', 'Info')])

    elif 'Info' == command[:4]:
        if command.count('=') == 0:
            set_admin_info(True)
            await bot.send_message(id, 'Отправьте 🆔 пользователя', buttons=Button.inline('❌Отмена', '⚜️Админка'))
        else:
            set_admin_info(False)
            user_id = int(command.split('=')[-1])
            template = [
                Button.inline('-10', f'Change={user_id}=-10'),
                Button.inline('-5', f'Change={user_id}=-5'),
                Button.inline('-1', f'Change={user_id}=-1'),
                Button.inline('+1', f'Change={user_id}=+1'),
                Button.inline('+5', f'Change={user_id}=+5'),
                Button.inline('+10', f'Change={user_id}=+10'),
            ]
            await bot.send_file(
                id,
                file=get_photo(user_id),
                parse_mode='HTML',
                caption=dict_to_str(get_user(user_id)),
                buttons=template
            )

    elif 'Show' == command[:4]:
        user_id = int(command.split('=')[-1])

        await bot.send_file(
            id,
            file=get_photo(user_id),
            parse_mode='HTML',
            caption=dict_to_str(get_user(user_id)),
            buttons=[Button.inline('Удалить анкету', 'Form=close')]
        )

    elif 'Change' == command[:6]:
        user_id = int(command.split('=')[1])
        x = int(command.split('=')[2])
        change_day(user_id, x)
        txt = f'Количество дней у `{user_id}` изменено на {x}\n'\
              f'Посдедний день подписки: {get_subscription(user_id)}'
        await bot.send_message(id, txt)

    elif 'Form' == command[:4]:
        stage = command.split('=')[-1]
        if stage == 'start':
            form_filling[id] = 1
            await event.edit('Введите Имя и Фамилию через пробел')
        elif stage == 'close':
            update_user(id, 'active', 0)
            await event.edit('Анкета удалена')

    elif 'Sex' == command[:3]:
        tmp = int(command.split('=')[-1])
        print(tmp)
        update_user(id, 'gender', tmp)
        form_filling[id] = 4
        await bot.send_message(id, 'Введите ваш город')

    elif 'Check' == command[:5]:
        payment_id = command.split('=')[-1]

        result = get_payment(payment_id)
        if result:
            user_id, amount, time = result.split('=')
            user_id, amount = int(user_id), int(amount)

            days = amount_to_days[amount]
            change_day(user_id, days)
            await event.delete()
            txt = 'Оплата прошла успешно\n\n'\
                  'Ссылка в разделе просмотра анкет станет действительной в течение минуты'
            await bot.send_message(id, txt)

            txt = '➕Новое зачисление\n'\
                  f'🆔: `{user_id}`\n'\
                  f'На сумму: {amount}💶'
            for admin_id in admins:
                try:
                    await bot.send_message(admin_id, txt)
                except ValueError:
                    pass
        else:
            txt = 'Оплата не прошла или ещё не подтверждена\nПовторите запрос позднее\n'\
                  'В случае ошибки свяжитесь с администратором'
            await event.delete()
            await bot.send_message(id, txt, buttons=[
                [Button.inline('Проверить оплату', command)],
                [Button.url('Администратор↗️', 'https://t.me/Ksenia_Kozlova_Italy')],
            ])

    elif 'Pay' == command[:3]:
        amount = int(command.split('=')[-1])
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            result = create_payment(id, amount, time)
        except Exception as e:
            result = False
            logging.error(str(e))

        await event.delete()
        if result:
            txt = f'Оплатить {amount}💶\nНе забудьте проверить оплату'
            await bot.send_message(id, txt, buttons=[
                [Button.url('✅Оплатить', result[0])],
                [Button.inline('Проверить оплату', f'Check={result[1]}')],
            ])
        else:
            txt = 'Оплата временно недоступна\nПриносим извинения за неудобства'
            await bot.send_message(id, txt, buttons=[
                Button.url('Связаться с администратором↗', 'https://t.me/Ksenia_Kozlova_Italy')
            ])

    elif 'Reject' == command[:6]:
        user_id = int(command.split('=')[-1])
        await event.delete()
        await bot.send_message(id, 'Запрос отклонён')

        if id == get_companion(user_id):
            update_user(user_id, 'chat_with', 0)
            if user_id in admins:
                await bot.send_message(user_id, 'Собеседник отклонил запрос', buttons=admin_keyboard)
            else:
                await bot.send_message(user_id, 'Собеседник отклонил запрос', buttons=main_keyboard)

    elif 'Dialog' == command[:6]:
        user_id = int(command.split('=')[-1])

        active = is_user_active(user_id)

        now = datetime.now()
        girl = is_user_girl(id)
        user_time = get_subscription(id)

        if user_time is None or user_time < now:
            enough_time = False
        else:
            enough_time = True

        if active:
            if girl or (not girl and enough_time):
                user_companion = get_companion(user_id)
                update_user(id, 'chat_with', user_id)
                if id == user_companion:
                    await bot.send_message(id, f'Начался диалог с {user_id}', buttons=dialog_keyboard)
                    await bot.send_message(user_id, f'Начался диалог с {id}', buttons=dialog_keyboard)
                elif user_companion == 0:
                    await bot.send_message(id, 'Отправлен запрос собеседнику', buttons=dialog_keyboard)
                    await bot.send_file(
                        user_id,
                        file=get_photo(id),
                        parse_mode='HTML',
                        caption=dict_to_str(get_user(id)),
                        buttons=[
                            Button.inline('Начать диалог', f'Dialog={id}'),
                            Button.inline('Отклонить', f'Reject={id}'),
                        ]
                    )
                else:
                    await bot.send_message(id, 'Пользователь на данный момент занят\nПопробуйте позднее')
            else:
                await bot.send_message(id, 'Необходимо оплатить подписку')
        else:
            await bot.send_message(id, 'К сожалению, анкета уже неактивна')
