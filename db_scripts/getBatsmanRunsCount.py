#!/usr/bin/python
import mysql.connector


def create_connection_mysql():
    """ create a database connection to a SQLite database """

    try:
        connection = mysql.connector.connect(host='localhost', database='CricketDb', user='user', password='password')
        print("connect successful!!")
        return connection
    except mysql.connector.Error as e:
        print(e)
    return None


def getRunCount(batsman,year):
    try:
        connection = create_connection_mysql()
        with connection.cursor() as cursor:

            # SQL
            sql = "select count(runs_batsman) from odi_ball_by_ball_v2 where  batsman_name like'%Kohli%' and year=2019"

            # Execute query.
            cursor.execute(sql)

            print("cursor.lastrowid: ", cursor.lastrowid)

            for row in cursor:
                print(row)

            # cursor.execute('''SELECT count(*) FROM odi_ball_by_ball ''')
            # return cursor.lastrowid

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
    getRunCount("Kohli",2019)
    # truncate_table()
