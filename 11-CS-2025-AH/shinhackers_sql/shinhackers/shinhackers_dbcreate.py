import sqlite3

conn = sqlite3.connect('shinhackers.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Games')

#Games table
cursor.execute('''
               CREATE TABLE Games
               (
                   Day    INT,
                   Month  INT,
                   Team   VARCHAR(50),
                   Ours   INT,
                   Theirs INT
               )
               ''')

games_data = [
    (7, 3, 'Toecrushers', 6, 25),
    (14, 3, 'Headbutters', 0, 10),
    (21, 3, 'Necktwsiters', 21, 10),
    (28, 3, 'Ankletappers', 18, 16),
    (4, 4, 'Armlockers', 0, 6),
    (11, 4, 'Kneeknockers', 0, 9),
    (18, 4, 'Bellyfloppers', 9, 3),
    (25, 4, 'Headbutters', 14, 6),
    (2, 5, 'Toecrushers', 6, 16)
]

cursor.executemany('''
                   INSERT INTO Games (Day, Month, Team, Ours, Theirs)
                   VALUES (?, ?, ?, ?, ?)''', games_data)

conn.commit()
conn.close()