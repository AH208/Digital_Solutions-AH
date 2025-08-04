import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('wiseacres_academic.db')

# Create a cursor object
cur = conn.cursor()

# Create Schools table
cur.execute('''
CREATE TABLE IF NOT EXISTS Schools (
    School_Id INTEGER PRIMARY KEY,
    School_Name TEXT,
    Phone TEXT,
    Head_Id INTEGER
)
''')

# Create Staff table
cur.execute('''
CREATE TABLE IF NOT EXISTS Staff (
    Staff_Id INTEGER PRIMARY KEY,
    Staff_Name TEXT,
    School_Id INTEGER,
    FOREIGN KEY (School_Id) REFERENCES Schools (School_Id)
)
''')

# Create Quals table
cur.execute('''
CREATE TABLE IF NOT EXISTS Quals (
    Staff_Id INTEGER,
    Degree TEXT,
    Place TEXT,
    Year INTEGER,
    PRIMARY KEY (Staff_Id, Degree, Place),
    FOREIGN KEY (Staff_Id) REFERENCES Staff (Staff_Id)
)
''')

# Insert data into Schools table
schools_data = [
    (1, 'School of Computer Science', '2299', 1),
    (2, 'School of Accountancy', '8756', 2),
    (3, 'School of Chemistry', '1869', None)
]
cur.executemany('INSERT INTO Schools (School_Id, School_Name, Phone, Head_Id) VALUES (?, ?, ?, ?)', schools_data)

# Insert data into Staff table
staff_data = [
    (1, 'Prof B. Tree', 1),
    (2, 'I. Drone', 1),
    (3, 'L.R. Parser', 1),
    (4, 'Ms C.R. Ledger', 2),
    (5, 'D. Fraud', 2),
    (6, 'M. Bezzle', 2),
    (7, 'P.P. Lounge-Lizard', 2),
    (8, 'C.A. Quick-Lime', 3),
    (9, 'A.G. Silver', 3),
    (10, 'H.H. Esso-Fore', 3)
]
cur.executemany('INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (?, ?, ?)', staff_data)

# Insert data into Quals table
quals_data = [
    (1, 'BSc', 'UW', 1925),
    (1, 'PhD', 'UQ', 1928),
    (2, 'BSc', 'UQ', 1979),
    (2, 'MSc', 'UNSW', 1984),
    (3, 'BAppSc', 'QIT', 1987),
    (4, 'Degree', 'QIT', 1972),
    (4, 'MBA', 'UWA', 1975),
    (5, 'BComm', 'UQ', 1995),
    (5, 'MBA', 'UCLA', 1998),
    (6, 'BBus', 'UW', 1989),
    (7, 'BBus', 'QUT', 1989),
    (7, 'MBA', 'UQ', 1992),
    (8, 'BSc', 'UNT', 1956),
    (8, 'PhD', 'UW', 1958),
    (9, 'BSc', 'UW', 1975),
    (9, 'MSc', 'UW', 1977),
    (9, 'PhD', 'UW', 1980),
    (10, 'BSc', 'MU', 1970),
    (10, 'PhD', 'UNT', 1974)
]
cur.executemany('INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (?, ?, ?, ?)', quals_data)

# Commit the changes
conn.commit()

# Close the connection
conn.close()
