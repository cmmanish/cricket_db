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

if __name__ == '__main__':
    create_connection_mysql()