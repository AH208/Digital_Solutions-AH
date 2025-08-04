from flask import render_template, Flask, g
import sqlite3

app = Flask(__name__)
DATABASE = 'witsend.db'

#Queries
#SELECT COUNT(*) FROM "Staff"
#SELECT Phone FROM "Staff" WHERE Teacher = "Hacker"
#SELECT Phone FROM Staff WHERE Teacher = (SELECT Teacher FROM allocation WHERE Subject = "Music")
#SELECT DISTINCT Teacher FROM allocation WHERE Theater = "Cramp"
#SELECT Subject FROM allocation WHERE Enrolled > (SELECT Capacity FROM Theaters WHERE Theaters.Theater = Allocation.Theater)
#SELECT Teacher FROM Staff WHERE Room = (SELECT Room FROM Staff WHERE Teacher = "Drone") AND Teacher !="DRONE"
#SELECT Theater FROM Theaters WHERE Theater NOT IN (SELECT DISTINCT Theater FROM allocation)
#SELECT Theater FROM Theaters WHERE Capacity > 25
#SELECT Theater FROM Theaters WHERE Capacity > (SELECT Capacity FROM Theaters WHERE Theater = "Chockers")
#SELECT Theater FROM Theaters WHERE Capacity >= (SELECT Enrolled FROM allocation WHERE Subject = "Singing")
#'"What are the names and phone numbers of teachers involved with subjects that are over-enrolled?":
#SELECT DISTINCT Staff.Teacher, Staff.Phone FROM Staff JOIN Allocation ON Staff.Teacher = Allocation.Teacher WHERE Allocation.Enrolled > (SELECT Capacity FROM Theaters WHERE Theaters.Theater = Allocation.Theater)"

def get_db():
   db = getattr(g, '_database', None)
   if db is None:
       db = g.database = sqlite3.connect(DATABASE)
   return db

@app.teardown_appcontext
def close_connection(exception):
   db = getattr(g, '_database', None)
   if db is not None:
       db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attributes')
def attributes():
    db = get_db()
    #Staff
    cur = db.execute("SELECT COUNT(*) FROM pragma_table_info('staff')")
    staff_count = cur.fetchone() [0]
    cur = db.execute("SELECT COUNT(*) FROM ('staff')")
    staff_tuple_count = cur.fetchone() [0]
    #allocation
    cur = db.execute("SELECT COUNT(*) FROM pragma_table_info('allocation')")
    allocation_count = cur.fetchone() [0]
    cur = db.execute("SELECT COUNT(*) FROM ('allocation')")
    allocation_tuple_count = cur.fetchone() [0]
    #Theaters
    cur = db.execute("SELECT COUNT(*) FROM pragma_table_info('Theaters')")
    theaters_count = cur.fetchone() [0]
    cur = db.execute("SELECT COUNT(*) FROM ('Theaters')")
    theaters_tuple_count = cur.fetchone() [0]
    return (f"There are {staff_count} attributes and {staff_tuple_count} tuples in the staff table.<br>"
    f"There are {allocation_count} attributes and {allocation_tuple_count} tuples in the staff table.<br>"
    f"There are {theaters_count} attributes and {theaters_tuple_count} tuples in the staff table.<br>"
        f"<a href='/'>Back to Home</a>")

@app.route('/hacker_ph')
def hacker_ph():
    db = get_db()
    cur = db.execute("SELECT Phone FROM Staff WHERE Teacher = ('Hacker')")
    hacker_ph = cur.fetchone()[0]
    #IF statement
    return (f"Hackers phone number is: {hacker_ph}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/music_teach_room')
def music_teach_room():
    db = get_db()
    cur = db.execute("""
        SELECT Staff.Phone, Allocation.Theater
        FROM Staff
        JOIN Allocation ON Staff.Teacher = Allocation.Teacher
        WHERE Allocation.Subject = 'Music'
    """)
    result = cur.fetchone()
    if result:
        phone, theater = result
        return (f"The music teacher's room is: {theater}<br>"
                f"And their phone number is: {phone}<br>"
                f"<a href='/'>Back to Home</a>")
    else:
        return ("Music teacher not found.<br>"
                "<a href='/'>Back to Home</a>")

@app.route('/cramp_teachers')
def cramp_teachers():
    db = get_db()
    cur = db.execute("SELECT DISTINCT Teacher FROM allocation WHERE Theater = ('Cramp')")
    teachers = cur.fetchall()
    teachers = [t[0] for t in teachers]
    return (f"The teacher that teach in cramp are: {teachers}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/over_enrollment_sub')
def over_enrollment_sub():
    db = get_db()
    cur = db.execute("SELECT Subject FROM allocation WHERE Enrolled > (SELECT Capacity FROM Theaters WHERE Theaters.Theater = Allocation.Theater)")
    subjects= cur.fetchall()
    subjects = [s[0] for s in subjects]
    return (f"The subjects with over-enrollment are {subjects}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/drone_teach_share')
def drone_teach_share():
    db = get_db()
    cur = db.execute("SELECT Teacher FROM Staff WHERE Room = (SELECT Room FROM Staff WHERE Teacher = Drone AND Teacher !=('DRONE')")
    teachers = cur.fetchall()
    teachers = [t[0] for t in teachers]
    return (f"The teachers that share a room with drone are: {teachers}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/theaters_empty')
def theaters_empty():
    db = get_db()
    cur = db.execute("SELECT Theater FROM Theaters WHERE Theater NOT IN (SELECT DISTINCT Theater FROM allocation)")
    theater = cur.fetchone()[0]
    return (f"Theaters empty: {theater}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/theaters_cap')
def theaters_cap():
    db = get_db()
    cur = db.execute("SELECT Theater FROM Theaters WHERE Capacity > 25")
    theaters = [t[0] for t in cur.fetchall()]
    return (f"Theaters with capacity over 25: {theaters}<br>"
    f"<a href='/'>Back to Home</a>")
    
@app.route('/theaters_cap_chock')
def theaters_cap_chock():
    db = get_db()
    cur = db.execute("""SELECT Theater FROM Theaters WHERE Capacity > (SELECT Capacity FROM Theaters WHERE Theater = "Chockers")""")
    theaters = [t[0] for t in cur.fetchall()]
    return (f"Theaters with capacity more than Chockers: {theaters}<br>"
    f"<a href='/'>Back to Home</a>")

#These two need 3 quotation marks at the end of the string for some reason

@app.route('/theaters_cap_sing')
def theaters_cap_sing():
    db = get_db()
    cur = db.execute("""SELECT Theater FROM Theaters WHERE Capacity >= (SELECT Enrolled FROM allocation WHERE Subject = "Singing")""")
    theaters = [t[0] for t in cur.fetchall()]
    return (f"Theaters that can hold the number of students enrolled in Singing: {theaters}<br>"
    f"<a href='/'>Back to Home</a>")

@app.route('/teacher_over_enrolled')
def teacher_over_enrolled():
    db = get_db()
    cur = db.execute("""
        SELECT DISTINCT Staff.Teacher, Staff.Phone, Allocation.Theater
        FROM Staff
        JOIN Allocation ON Staff.Teacher = Allocation.Teacher
        WHERE Allocation.Enrolled > (
            SELECT Capacity FROM Theaters WHERE Theaters.Theater = Allocation.Theater
        )
    """)
    teachers = cur.fetchall()
    if teachers:
        formatted = "<br>".join([f"{t[0]} ({t[1]}) in {t[2]}" for t in teachers])
        return f"Teachers with over-enrolled subjects:<br>{formatted}<br><a href='/'>Back to Home</a>"
    else:
        return ("No teachers found with over-enrolled subjects.<br>"
                "<a href='/'>Back to Home</a>")

# the last one is AI suggestion, tuple to list or list comprehension :)

#SELECT DISTINCT Staff.Teacher, Staff.Phone FROM Staff JOIN Allocation ON Staff.Teacher = Allocation.Teacher WHERE Allocation.Enrolled > (SELECT Capacity FROM Theaters WHERE Theaters.Theater = Allocation.Theater)

# cool, I think I am all done

if __name__ == '__main__':
    app.run(debug=True)