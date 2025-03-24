from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = 'Games.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        try:
            db.close()
        except sqlite3.Error as e:
            print(f"Database close error: {e}")

@app.route("/")
def index():
    try:
        db = get_db()
        if db is None:
            return "Database connection error", 500

        cursor = db.cursor()
        sql = """
            SELECT 
                games.game_id,
                games.game_title, 
                games.price, 
                games.release_date, 
                rating.label as age_rating, 
                games.game_maker,
                games.player_count
            FROM games
            JOIN rating ON games.age_rating = rating.rating_id
            WHERE 1=1  -- Start with a true condition
        """
        params = []

        age_rating = request.args.get('age_rating')
        price = request.args.get('price')

        if age_rating:
            sql += " AND rating.label = ?"
            params.append(age_rating)

        if price:
            sql += " AND games.price = ?"
            params.append(price)

        cursor.execute(sql, params)
        results = cursor.fetchall()

        cursor.execute("SELECT DISTINCT label FROM rating ORDER BY display_order")
        age_ratings = [row['label'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT price FROM games ORDER BY price")
        prices = [row['price'] for row in cursor.fetchall()]

        print("Results:", results)
        return render_template(
            "index.html",
            games=results,
            age_rating_filter=age_rating,
            price_filter=price,
            age_ratings=age_ratings,
            prices=prices,
        )
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return "Database query error", 500  
    except Exception as e:
        print(f"General error: {e}")
        return "Internal server error", 500

if __name__ == "__main__":
    app.run(debug=True)