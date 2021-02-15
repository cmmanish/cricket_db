from flask import Flask, request, jsonify, Response
import mysql.connector

app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='127.0.0.1', port='3306', password='password', database='CricketDb')

@app.route("/")
def hello():
    db = getMysqlConnection()
    print(db)
    try:
        sqlstr = "SELECT * from odi_ball_by_ball;"
        print(sqlstr)
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify(results=output_json)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')