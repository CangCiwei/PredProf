import matplotlib.pyplot as plt
import sqlite3

db = sqlite3.connect("./database.db")
cursor = db.cursor()

def zadanie_3():
    a = []
    k = 0
    t = 0
    for step in range(313):
        for row in cursor.execute("SELECT * FROM apartment_temperature"):
            if row[0] == 1:
                if row[4] == step:
                    print(row)
                    k += 1
                    t += row[5]
        a.append(t/k)
        t = 0
        k = 0
    return a

def zadanie_4():
    a = []
    b = []
    city = 0
    for apartment in [166, 75, 11, 53, 5, 34, 33, 69, 129, 89, 21, 5, 22, 5, 12, 1]:
        for step in range(313):
            for row in cursor.execute("SELECT * FROM apartment_temperature"):
                if row[0] == city + 1:
                    if row[4] == step:
                        if row[3] == apartment:
                            print(row)
                            b.append(row[5])        
        a.append(b)
        b = []
        city += 1
    return a

def zadanie_5():
    a = []
    b = []
    c = []
    for area in [1,5,6,4,4]:
        for step in range(313):
            for row in cursor.execute("SELECT * FROM apartment_temperature"):
                if (row[0] == 1) and (row[1] == area) and (row[4] == step):
                    b.append(row[5])  
                    print(row)
            a.append(max(b))
            b = []
        c.append(a)
        a = []  
    return c


fig, ax = plt.subplots()  
plt.xlabel('Время')
plt.ylabel('Значение температуры')
plt.title("Среднее значение температур в квартирах")
ax.plot(range(313), zadanie_3())

z4 = zadanie_4()
for i in [0,1,2,3,4,5,7,8,9,11,12,13,14,15]:
    fig, ax = plt.subplots()  
    plt.xlabel('Время')
    plt.ylabel('Значение температуры')
    plt.title("Значение температуры в квартире")
    ax.plot(range(313), z4[i])    
for i in [6,10]:
    fig, ax = plt.subplots()  
    plt.xlabel('Время')
    plt.ylabel('Значение температуры')
    plt.title("Значение температуры в квартире")
    ax.plot(range(626), z4[i])
    
z5 = zadanie_5()
for i in z5:
    fig, ax = plt.subplots()  
    plt.xlabel('Время')
    plt.ylabel('Значение температуры')
    plt.title("Среднее значение температур в квартирах")
    ax.plot(range(313), i)
