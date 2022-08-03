amount_to_days = {
    10: 10,
}

users_list = set()
form_filling = dict()


def map_url(x, y):
    return f'<a href="http://maps.google.com/maps?q={x},{y}+(My+Point)&z=14&ll={x},{y}">Open in Google Maps</a>'


def dict_to_str(d):
    txt = ''
    txt += f'🆔: {d["user_id"]} | USERNAME = @{d["username"]}\n'
    txt += f'Имя: {d["f_name"]} {d["l_name"]} | Возраст: {d["age"]}\n' \
           f'Город: {d["city"]}\n'
    if d["gender"] == 0 or d["gender"] == '0':
        txt += 'Пол: мужской\n'
    else:
        txt += 'Пол: женский\n'
    if d["latitude"] is not None:
        txt += map_url(d["latitude"], d["longitude"]) + '\n'
    txt += f'О себе:\n{d["about"]}\n'

    return txt
