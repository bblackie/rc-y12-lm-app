from flask import Flask, g, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'Games.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    cursor = get_db().cursor()
    sql = "SELECT * FROM games"
    cursor.execute(sql)
    results = cursor.fetchall
    
    print(results)

    return render_template("index.html", games=results)     

if __name__ == "__main__":
    app.run(debug=True)