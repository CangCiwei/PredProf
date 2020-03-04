# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 16:30:06 2020

@author: user
"""

import sqlite3

a = sqlite3.connect("./abcde.db")

c = a.cursor()

#c.execute("""CREATE TABLE abcd1
#             (id int, ttextt text, txt text)
#          """)

#c.execute("""INSERT INTO abcd1 VALUES (4, 'лай-лай', 'нана-нана')""")

#a.commit()

#c.execute("""UPDATE abcd1 SET txt = 'ой-ю-ёй' WHERE txt = 'ляля-ляля'""")
#a.commit()

#c.execute("SELECT * FROM abcd1")
#print(c.fetchall())

for i in c.execute("SELECT * FROM abcd1"):
    print(f"{i[0]} {i[1]} {i[2]}")
