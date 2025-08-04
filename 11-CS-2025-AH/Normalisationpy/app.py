from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    dob = request.form.get('dob', '')
    street = request.form.get('street', '')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code', '')
    country = request.form.get('country', '')
    emergency_contact_name = request.form.get('emergency_contact_name', '')
    emergency_contact_phone = request.form.get('emergency_contact_phone', '')
    conn = sqlite3.connect('normal.sqlite3')
    cursor = conn.cursor()
    # inserts the user details in the users table
    cursor.execute('INSERT INTO users (first_name, last_name, email, phone, dob, street, city, state, zip_code, country) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (first_name, last_name, email, phone, dob, street, city, state, zip_code, country))
    # emergency_contact_name, emergency_contact_phone
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database
    studentname = f"{first_name} {last_name}"

    return (f"Received data: First Name={first_name}, Last Name={last_name}, Email={email}, "
            f"Phone={phone}, Date of Birth={dob}, Address={street}, {city}, {state}, {zip_code}, {country}, "
            f"Emergency Contact Name={emergency_contact_name}, Emergency Contact Phone={emergency_contact_phone}")

if __name__ == '__main__':
    app.run(debug=True)