#!/usr/bin/python
import mysql.connector

from db_scripts.mysql_connect import create_connection_mysql


def getRowCount():
    try:
        connection = create_connection_mysql()
        with connection.cursor() as cursor:
            # SQL
            sql = "select count(*) from odi_ball_by_ball;"
            # Execute query.
            cursor.execute(sql)
            print("cursor.lastrowid: ", cursor.lastrowid)
            for row in cursor:
                print(row)
    finally:
        connection.close()


def truncate_table():
    try:
        connection = create_connection_mysql()
        with connection.cursor() as cursor:

            sql = "TRUNCATE TABLE odi_ball_by_ball"
            # Execute query.
            cursor.execute(sql)
            print("cursor.lastrowid: ", cursor.lastrowid)

    except mysql.connector.Error as e:
        connection.rollback()
        print(e)

    finally:
        connection.close()


if __name__ == '__main__':
    getRowCount()
    truncate_table()
