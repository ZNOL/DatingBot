# import pymysql
import MySQLdb.cursors
import MySQLdb as pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE


def show_table():
    with pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
    ) as con:
        db_query = 'DESCRIBE users'
        with con.cursor() as cursor:
            cursor.execute(db_query)
            result = cursor.fetchall()
            for row in result:
                print(row)


def create_table():
    with pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor
    ) as con:
        drop_users_table_query = 'DROP TABLE IF EXISTS `users`'
        create_users_table_query = '''
                CREATE TABLE `users` (
                    `user_id` int NOT NULL PRIMARY KEY,
                    `username` varchar(45) DEFAULT NULL,
                    `f_name` varchar(45) DEFAULT NULL,
                    `l_name` varchar(45) DEFAULT NULL,
                    `age` int DEFAULT NULL,
                    `gender` varchar(25) DEFAULT NULL,
                    `city` varchar(25) DEFAULT NULL,
                    `latitude` double DEFAULT NULL,
                    `longitude` double DEFAULT NULL,
                    `about` varchar(255) DEFAULT NULL,
                    `photo` varchar(150) DEFAULT NULL,
                    `subscription` datetime DEFAULT NULL,
                    `active` int DEFAULT 0,
                    `is_fake` int DEFAULT 0,
                    `chat_with` int DEFAULT 0
                );
                '''
        with con.cursor() as cursor:
            cursor.execute(drop_users_table_query)
            con.commit()
            cursor.execute(create_users_table_query)
            con.commit()

