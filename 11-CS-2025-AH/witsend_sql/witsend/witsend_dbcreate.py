import sqlite3

conn = sqlite3.connect('witsend.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Staff')
cursor.execute('DROP TABLE IF EXISTS Theaters')
cursor.execute('DROP TABLE IF EXISTS Allocation')

# May need Staff ID later
cursor.execute('''
CREATE TABLE IF NOT EXISTS Staff (
    Teacher TEXT PRIMARY KEY,
    Room TEXT,
    Phone TEXT
)
''')

#Theater table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Theaters (
    Theater TEXT PRIMARY KEY,
    Capacity INTEGER
)
''')

# if all goes wrong: Allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
# Allocation table
cursor.execute('''
CREATE TABLE IF NOT EXISTS allocation (
    Subject TEXT,
    Enrolled INTEGER,
    Theater TEXT,
    Teacher TEXT,
    FOREIGN KEY (Theater) REFERENCES Theaters (Theater),
    FOREIGN KEY (Teacher) REFERENCES Staff (Teacher)
)
''')

staff_data = [
    ('Drone',  '21', '2240'),
    ('Slack', '16', None),
    ('Tripp', '21', '2240'),
    ('Hacker', '18', '2868')
]

cursor.executemany('''
INSERT INTO Staff (Teacher, Room, Phone)
VALUES (?, ?, ?)
''', staff_data)

theater_data = [
    ('Tiny', 15),
    ('Chockers', 20),
    ('Cramp', 15),
    ('Cosy', 30)
]

print(type(theater_data)) #List
print(type(theater_data[0])) #tuple
print(type(theater_data[0][0])) #string
print(type(theater_data[0][1])) #integer

cursor.executemany('''
INSERT INTO Theaters (Theater, Capacity)
VALUES (?, ?)''', theater_data)

allocation_data = [
    ('Music', 10, 'Tiny', 'Drone'),
    ('Ballet', 25, 'Cosy', 'Tripp'),
    ('TapDancing', 35, 'Cosy', 'Tripp'),
    ('Programming', 10, 'Cramp', 'Hacker'),
    ('Singing', 25, 'Tiny', 'Drone' ),
    ('Surgery', 15, 'Cramp', 'Hacker' ),
    ('Poetry', 10, 'Cramp', 'Drone')
]

cursor.executemany('''
INSERT INTO allocation (Subject, Enrolled, Theater, Teacher)
VALUES (?, ?, ?, ?)''', allocation_data)

conn.commit()

conn.close()