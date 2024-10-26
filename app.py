import time
import mariadb
import os
import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

while True:
    try:
        conn = mariadb.connect(
            user="root",
            password=os.environ["MARIADB_ROOT_PASSWORD"],
            host="mariadbb",
            port=3306,
            database=os.environ["MARIADB_DATABASE"]
        )
        break
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        time.sleep(2)

cur = conn.cursor()
cur.execute("CREATE TABLE table1 (id INT AUTO_INCREMENT PRIMARY KEY,datetime DATETIME,client_info VARCHAR(255))")

@app.route('/')
def hello():
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now()
    cur.execute('INSERT INTO table1 (datetime, client_info) values (?, ?)', (current_time, user_agent))
    cur.execute("SELECT * FROM table1")
    rows = cur.fetchall()
    results = []
    for row in rows:
        results.append({
            'id': row[0],
            'timestamp': row[1].isoformat(),
            'user_agent': row[2]
        })
    conn.commit()
    return jsonify(results)