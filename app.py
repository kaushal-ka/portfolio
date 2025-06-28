from flask import Flask, request, redirect, render_template, jsonify, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'a2bbd46e9bb70cc4842adf4b34f54f06'  # Replace with a secure key

# Database configuration
db_config = {
    'user': 'root',        # Replace with your DB username
    'password': 'Kaushal@1234',  # Replace with your DB password
    'host': 'localhost',
    'database': 'portfolio_db'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Retrieve form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    print(f"Name: {name}, Email: {email}, Message: {message}")
    # Basic validation can be added here if needed
    if not name or not email or not message:
        # flash("All fields are required!")
        # return redirect(url_for('index'))
        return jsonify(status="error", message="All fields are required!"), 400
    

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()

            # SQL query to insert data into the 'contacts' table
            query = """
                INSERT INTO contacts (name, email, message)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, email, message))
            conn.commit()  # Commit the transaction

            # Close cursor and connection
            cursor.close()
            conn.close()
            #including jsonify response
            return jsonify(
                status = "success",
                message = "Thank you for your message! I'll get back to you soon.")
    except mysql.connector.Error as err:
            return jsonify(status ="error", message = f"Database error: {err}"), 500
            # <-- Here: flash success message after DB insert
        #     flash("Thank you for your message! I'll get back to you soon.")
        # else:
        #     flash("Unable to connect to the database.")
    # except mysql.connector.Error as err:
    #     print("MySQL Error:", err)
    #     flash(f"An error occurred: {err}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
