import mysql.connector
from flask import Flask
from flask import jsonify

app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='user', host='mysql_db', port='3306', password='password', database='cricketdb')

@app.route("/")
def hello():
    db = getMysqlConnection()
    print(db)
    try:
        sqlstr = "SELECT count(*) from odi_ball_by_ball;"
        print(sqlstr)
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify(results=output_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
