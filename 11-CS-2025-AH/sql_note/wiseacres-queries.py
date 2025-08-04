import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('wiseacres_academic.db')

# Create a cursor object
cur = conn.cursor()

# Query to return all data from the Schools table
def get_all_schools():
    cur.execute('SELECT * FROM Schools')
    return cur.fetchall()

# Query to return all data from the Staff table
def get_all_staff():
    cur.execute('SELECT * FROM Staff')
    return cur.fetchall()

# Query to return all data from the Quals table
def get_all_quals():
    cur.execute('SELECT * FROM Quals')
    return cur.fetchall()

# Query to return staff and their qualifications
def get_staff_qualifications():
    cur.execute('''
    SELECT Staff.Staff_Name, Quals.Degree, Quals.Place, Quals.Year
    FROM Staff
    JOIN Quals ON Staff.Staff_Id = Quals.Staff_Id
    ''')
    return cur.fetchall()

# Query to return staff details by school
def get_staff_by_school(school_id):
    cur.execute('''
    SELECT Staff.Staff_Name, Schools.School_Name
    FROM Staff
    JOIN Schools ON Staff.School_Id = Schools.School_Id
    WHERE Schools.School_Id = ?
    ''', (school_id,))
    return cur.fetchall()

# Query to return the head of each school
def get_school_heads():
    cur.execute('''
    SELECT Schools.School_Name, Staff.Staff_Name AS Head_Name
    FROM Schools
    JOIN Staff ON Schools.Head_Id = Staff.Staff_Id
    ''')
    return cur.fetchall()

# Fetch and print results
print("All Schools:")
print(get_all_schools())

print("\nAll Staff:")
print(get_all_staff())

print("\nAll Qualifications:")
print(get_all_quals())

print("\nStaff Qualifications:")
print(get_staff_qualifications())

print("\nStaff by School (School ID = 1):")
print(get_staff_by_school(1))

print("\nSchool Heads:")
print(get_school_heads())

# Close the connection
conn.close()
