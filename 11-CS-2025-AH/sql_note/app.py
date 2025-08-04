from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('wiseacres_academic.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    print("Connected to database")
    schools = conn.execute('SELECT * FROM Schools').fetchall()
    #rows_as_dicts = [dict(row) for row in schools]
    schools = [dict(row) for row in schools]
    print("School:", schools)
    staff = conn.execute('SELECT * FROM Staff').fetchall()
    staff = [dict(row) for row in staff]
    print("Staff:", staff)
    quals = conn.execute('SELECT * FROM Quals').fetchall()
    quals = [dict(row) for row in quals]
    print("Quals:", quals)
    conn.close()
    print("Connection closed")
    return render_template('index.html', schools=schools, staff=staff, quals=quals)

@app.route('/staff_qualifications')
def staff_qualifications():
    conn = get_db_connection()
    staff_qualifications = conn.execute('''
    SELECT Staff.Staff_Name, Quals.Degree, Quals.Place, Quals.Year
    FROM Staff
    JOIN Quals ON Staff.Staff_Id = Quals.Staff_Id
    ''').fetchall()
    conn.close()

    # Organize data into a dictionary
    staff_qualifications_dict = {}  # Create an empty dictionary
    for row in staff_qualifications:  # Iterate through the rows of the staff_qualifications list
        staff_name = row['Staff_Name']  # Get the staff name from the current row
        qualification = {
            'Degree': row['Degree'],
            'Place': row['Place'],
            'Year': row['Year']
        }
        print(type(staff_name))
        print(type(qualification))
        if staff_name not in staff_qualifications_dict:
            staff_qualifications_dict[staff_name] = []
        staff_qualifications_dict[staff_name].append(qualification)

    return render_template('staff_qualifications1.html', staff_qualifications=staff_qualifications_dict)

@app.route('/school_heads')
def school_heads():
    conn = get_db_connection()
    cursor = conn.cursor()
    staff_by_school = conn.execute('''
    SELECT Schools.School_Name, Staff.Staff_Name AS Head_Name
    FROM Schools
    JOIN Staff ON Schools.Head_Id = Staff.Staff_Id
    ''')
    school_heads = cursor.fetchall()
    print(school_heads)
    school_heads = [dict(zip([column[0] for column in cursor.description], row)) for row in school_heads]

    cursor.close()
    conn.close()

    staff_heads = {}  # Create an empty dictionary
    for row in school_heads:  # Iterate through the rows of the staff_qualifications list
        staff_name = row['Head_Name']  # Get the staff name from the current row
        school_name = row['School_Name']
        print(type(staff_name))
        print(type(school_heads))
        if school_heads not in school_heads:
            school_heads[staff_name] = []
        #school_heads_dict[staff_name]

    return render_template('school_heads.html', school_heads=school_heads)


@app.route('/staff_by_school/<int:school_id>')
def staff_by_school(school_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Staff.Staff_Name, Schools.School_name
    FROM Staff
    JOIN Schools ON Staff.School_Id = Schools.school_id
    WHERE Schools.school_id = ?
    ''', (school_id,))

    staff_by_school = cursor.fetchall()
    staff_by_school = [dict(zip([column[0] for column in cursor.description], row)) for row in staff_by_school]

    cursor.close()
    conn.close()

    return render_template('staff_by_school.html', staff_by_school=staff_by_school)


if __name__ == '__main__':
    app.run(port=5001, debug=True)