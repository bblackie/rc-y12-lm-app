from flask import Flask, g
import sqlite3

app = Flask(__name__)

DATABASE = 'Games.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    cursor = get_db().cursor()
    sql = "SELECT * FROM contents"
    cursor.execute(sql)
    results = cursor.fetchall()
    return str([dict(row) for row in results])

if __name__ == "__main__":
    app.run(debug=True)