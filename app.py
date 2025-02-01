from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'user': 'root',  # Change as per your MySQL setup
    'password': 'Likith@22',  # Change as per your MySQL setup
    'host': 'localhost',
    'database': 'sample_schema'
}

# Route for the registration form
@app.route("/")
def index():
    return render_template("register.html")

# Route to handle form submission
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Prevent SQL Injection by using parameterized queries
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, email))
        conn.commit()

        flash("Registration successful!", "success")
        return redirect("/")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            flash("Something is wrong with your username or password.", "error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            flash("Database does not exist.", "error")
        else:
            flash(f"Error: {err}", "error")
    finally:
        if 'conn' in locals():
            conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
