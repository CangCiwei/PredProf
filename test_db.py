# -*- coding: utf-8 -*-
import os
import sqlite3

"""create d"""
db_filename = './test.db'
conn = sqlite3.connect(db_filename)

"""BEGIN TRANSACTION;

/* Create a table called NAMES */
CREATE TABLE NAMES(Id integer PRIMARY KEY, Name text);

/* Create few records in this table */
INSERT INTO NAMES VALUES(1,'Tom');
INSERT INTO NAMES VALUES(2,'Lucy');
INSERT INTO NAMES VALUES(3,'Frank');
INSERT INTO NAMES VALUES(4,'Jane');
INSERT INTO NAMES VALUES(5,'Robert');
COMMIT;

/* Display all the records from the table */
SELECT * FROM NAMES;"""

script = "SELECT * FROM NAMES;"
cursor = conn.cursor()
cursor.execute(script)
#print(conn.executescript(script))
for row in cursor.fetchall():
    print(row)
conn.close()
