import psutil
import sqlite3
from datetime import datetime

connect = sqlite3.connect("System_monitoring.db")
cursor = connect.cursor()

try:
    cursor.execute("""CREATE TABLE InfoSystem
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    CPU TEXT,
                    RAM TEXT,
                    SWAP TEXT,
                    date TEXT)
                    """)
    connect.commit()
except sqlite3.OperationalError:
    pass

print("Приложение 'Системный монитор' ")
while True:
    print("1 - Вывести инфомацию по системе \n"
          "2 - Просмотр сохранёных данных\n"
          "3 - Выход")

    action = int(input("Выберите действие: "))

    if action == 1:
        RAM = psutil.virtual_memory()
        SWAP = psutil.disk_usage('/')
        CPU = psutil.cpu_percent()
        print(f"CPU загружен на {CPU}%")
        print(f"Оперативной памяти использованно: {round(RAM[3]/1073741824,1)} Гб")
        print(f"Диск загружен на {SWAP[3]}%\n")
        now = datetime.now()
        date = now.strftime("%Y-%m-%d,%H:%M")

        cursor.execute("""
               INSERT INTO InfoSystem
               (CPU, RAM, SWAP, date)
               VALUES (?, ?, ?, ?)
               """, (
            CPU,
            round(RAM[3]/1073741824,1),
            SWAP[3],
            date
        ))
        connect.commit()

    elif action == 2:
        cursor.execute("SELECT * FROM InfoSystem")
        all_rows = cursor.fetchall()
        print("История измерений: ")
        for row in all_rows:
            print(f"CPU загружен на {row[1]}%\n"
                  f"Оперативной памяти использованно: {row[2]} Гб\n"
                  f"Диск загружен на {row[3]}%\n"
                  f"Время измерений: {row[4]}\n")

    elif action == 3:
        break

    else:
        print("Действие не выбранно")
