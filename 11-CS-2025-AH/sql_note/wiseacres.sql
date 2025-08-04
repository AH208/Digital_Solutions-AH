-- To create run the following at Terminal
-- sqlite3 wiseacres.db < wiseacres.sql

-- Create Schools table
CREATE TABLE IF NOT EXISTS Schools (
    School_Id INTEGER PRIMARY KEY,
    School_Name TEXT,
    Phone TEXT,
    Head_Id INTEGER
);

-- Create Staff table
CREATE TABLE IF NOT EXISTS Staff (
    Staff_Id INTEGER PRIMARY KEY,
    Staff_Name TEXT,
    School_Id INTEGER,
    FOREIGN KEY (School_Id) REFERENCES Schools (School_Id)
);

-- Create Quals table
CREATE TABLE IF NOT EXISTS Quals (
    Staff_Id INTEGER,
    Degree TEXT,
    Place TEXT,
    Year INTEGER,
    PRIMARY KEY (Staff_Id, Degree, Place),
    FOREIGN KEY (Staff_Id) REFERENCES Staff (Staff_Id)
);

-- Insert data into Schools table
INSERT INTO Schools (School_Id, School_Name, Phone, Head_Id) VALUES (1, 'School of Computer Science', '2299', 1);
INSERT INTO Schools (School_Id, School_Name, Phone, Head_Id) VALUES (2, 'School of Accountancy', '8756', 2);
INSERT INTO Schools (School_Id, School_Name, Phone, Head_Id) VALUES (3, 'School of Chemistry', '1869', NULL);

-- Insert data into Staff table
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (1, 'Prof B. Tree', 1);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (2, 'I. Drone', 1);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (3, 'L.R. Parser', 1);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (4, 'Ms C.R. Ledger', 2);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (5, 'D. Fraud', 2);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (6, 'M. Bezzle', 2);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (7, 'P.P. Lounge-Lizard', 2);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (8, 'C.A. Quick-Lime', 3);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (9, 'A.G. Silver', 3);
INSERT INTO Staff (Staff_Id, Staff_Name, School_Id) VALUES (10, 'H.H. Esso-Fore', 3);

-- Insert data into Quals table
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (1, 'BSc', 'UW', 1925);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (1, 'PhD', 'UQ', 1928);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (2, 'BSc', 'UQ', 1979);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (2, 'MSc', 'UNSW', 1984);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (3, 'BAppSc', 'QIT', 1987);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (4, 'Degree', 'QIT', 1972);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (4, 'MBA', 'UWA', 1975);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (5, 'BComm', 'UQ', 1995);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (5, 'MBA', 'UCLA', 1998);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (6, 'BBus', 'UW', 1989);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (7, 'BBus', 'QUT', 1989);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (7, 'MBA', 'UQ', 1992);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (8, 'BSc', 'UNT', 1956);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (8, 'PhD', 'UW', 1958);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (9, 'BSc', 'UW', 1975);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (9, 'MSc', 'UW', 1977);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (9, 'PhD', 'UW', 1980);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (10, 'BSc', 'MU', 1970);
INSERT INTO Quals (Staff_Id, Degree, Place, Year) VALUES (10, 'PhD', 'UNT', 1974);