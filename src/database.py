from src.bot import *
from src.users import *
from datetime import datetime, timedelta
from src.database_start import *


def execute(sql, values=None):
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(sql, values)
                con.commit()
            except Exception as e:
                logging.error(str(e))


def add_user(user_id, username):
    sql = 'INSERT INTO users (user_id, username) VALUES (%s, %s)'
    values = (user_id, username)
    execute(sql, values)
    users_list.add(user_id)
    logging.info(f'{username} ({user_id}) joined')


def update_user(user_id, field_to_update, new_value):
    sql = f'UPDATE users SET {field_to_update} = %s WHERE user_id = %s'
    execute(sql, (new_value, user_id))


def get_companion(user_id):
    sql = f'SELECT chat_with FROM users WHERE user_id = {user_id}'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()["chat_with"]
    return int(result)


def get_subscription(user_id):
    sql = f'SELECT subscription FROM users WHERE user_id = {user_id}'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()["subscription"]
    return result


def change_day(user_id, x):
    now = datetime.now()
    time = get_subscription(user_id)
    if time is None:
        cur_time = now
    else:
        if time < now:
            cur_time = now
        else:
            cur_time = time

    new_time = cur_time + timedelta(days=x)
    update_user(user_id, 'subscription', new_time.strftime('%Y-%m-%d %H:%M:%S'))


def get_photo(user_id):
    sql = f'SELECT photo FROM users WHERE user_id = {user_id}'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()["photo"]
    return result


def is_user_girl(user_id):
    sql = f'SELECT gender FROM users WHERE user_id = {user_id}'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()["gender"]
    return result == 1 or result == '1'


def is_user_active(user_id):
    sql = f'SELECT active FROM users WHERE user_id = {user_id}'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(sql)
                result = cursor.fetchone()["active"]
            except TypeError:
                result = False
    return bool(result)


def get_user(user_id):
    sql = 'SELECT user_id, username, f_name, l_name, age, gender, city, latitude, longitude, about, photo, ' \
          'subscription, active, is_fake FROM users WHERE user_id = %s'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(sql, (user_id, ))
                return cursor.fetchone()
            except Exception as e:
                logging.error(str(e))


def get_users():
    sql = 'SELECT user_id, username, subscription, active, is_fake, chat_with FROM users'
    with pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                logging.error(str(e))


try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )
    for row in get_users():
        users_list.add(row['user_id'])
    logging.info('База успешно загружена')
except:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )
    # create_table()
    # create_db_query = f'CREATE DATABASE {DB_DATABASE}'
    # with connection as con:
    #     with con.cursor() as cursor:
    #         cursor.execute(create_db_query)
    # create_table()
    logging.info('База успешно создана')
