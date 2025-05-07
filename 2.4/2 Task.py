import sqlite3

def connect_date_base():
    return sqlite3.connect("Love_drink.db")

def create_tables():
    connect = connect_date_base()
    cursor = connect.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Drinks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        is_alcoholic BOOLEAN,
        price REAL,
        strength REAL,
        volume REAL CHECK (volume >= 0))
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        quantity INTEGER CHECK (quantity >= 0))
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cocktails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            strength REAL,
            price REAL
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cocktail_Components (
            cocktail_id INTEGER,
            component_type TEXT,
            component_name TEXT,
            quantity REAL,
            FOREIGN KEY (cocktail_id) REFERENCES Cocktails(id)
        )""")
    connect.commit()
    connect.close()

def add_cocktail(name, price, components):
    connect = connect_date_base()
    cursor = connect.cursor()
    total_alcohol = 0.0
    total_volume = 0.0

    for component in components:
        type_ = component['type']
        name_ = component['name']
        quantity = component['quantity']

        if type_ == 'Drink':
            cursor.execute("SELECT is_alcoholic, strength FROM Drinks WHERE name = ?", (name_,))
            drink = cursor.fetchone()
            if not drink:
                print(f"Напиток {name_} не найден!")
                connect.close()
                return
            if drink[0]:  # is_alcoholic
                total_alcohol += drink[1] * quantity
                total_volume += quantity
        elif type_ == 'Ingredient':
            cursor.execute("SELECT 1 FROM Ingredients WHERE name = ?", (name_,))
            if not cursor.fetchone():
                print(f"Ингредиент {name_} не найден!")
                connect.close()
                return

    strength = total_alcohol / total_volume if total_volume > 0 else 0

    try:
        cursor.execute("INSERT INTO Cocktails (name, strength, price) VALUES (?, ?, ?)",
                       (name, strength, price))
        cocktail_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        print("Коктейль с таким именем уже существует!")
        connect.close()
        return

    for component in components:
        cursor.execute("""INSERT INTO Cocktail_Components 
                       (cocktail_id, component_type, component_name, quantity)
                       VALUES (?, ?, ?, ?)""",
                       (cocktail_id, component['type'], component['name'], component['quantity']))

    connect.commit()
    connect.close()
    print("Коктейль успешно добавлен!")

def add_drink(name,price,is_alcoholic,volume,strength):
    connect = connect_date_base()
    cursor = connect.cursor()
    cursor.execute("""
                    INSERT INTO Drinks 
                    (name,price,strength,volume,is_alcoholic)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                    name,
                    price,
                    strength,
                    volume,
                    is_alcoholic
    ))
    connect.commit()
    connect.close()

def add_ingredient(name,quantity):
    connect =  connect_date_base()
    cursor = connect.cursor()
    cursor.execute("""
                    INSERT INTO Ingredients 
                    (name, quantity)
                    VALUES (?, ?)
                    """, (
                    name,
                    quantity
    ))
    connect.commit()
    connect.close()


def sell_cocktail(name):
    connect = connect_date_base()
    cursor = connect.cursor()

    cursor.execute("SELECT id FROM Cocktails WHERE name = ?", (name,))
    cocktail = cursor.fetchone()
    if not cocktail:
        print("Коктейль не найден!")
        connect.close()
        return

    cursor.execute("""SELECT component_type, component_name, quantity 
                   FROM Cocktail_Components WHERE cocktail_id = ?""", (cocktail[0],))
    components = cursor.fetchall()

    for component in components:
        type_, name_, quantity = component
        if type_ == 'Drink':
            cursor.execute("SELECT volume FROM Drinks WHERE name = ?", (name_,))
            volume = cursor.fetchone()[0]
            if volume < quantity:
                print(f"Недостаточно напитка {name_}!")
                connect.close()
                return
        elif type_ == 'Ingredient':
            cursor.execute("SELECT quantity FROM Ingredients WHERE name = ?", (name_,))
            ingredient = cursor.fetchone()[0]
            if ingredient < quantity:
                print(f"Недостаточно ингредиента {name_}!")
                connect.close()
                return
    try:
        for component in components:
            type_, name_, quantity = component
            if type_ == 'Drink':
                cursor.execute("UPDATE Drinks SET volume = volume - ? WHERE name = ?",
                               (quantity, name_))
            elif type_ == 'Ingredient':
                cursor.execute("UPDATE Ingredients SET quantity = quantity - ? WHERE name = ?",
                               (quantity, name_))
        connect.commit()
        print("Продажа успешно завершена!")
    except:
        connect.rollback()
        print("Ошибка при списании!")

def show_cocktails():
    connect = connect_date_base()
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM Cocktails")
    cocktails = cursor.fetchall()

    print("Список коктейлей:")
    for cocktail in cocktails:
        print(f"Название: {cocktail[1]}\n"
              f"Крепость: {cocktail[2]}%\n"
              f"Цена: {cocktail[3]}")

        cursor.execute("""SELECT component_type, component_name, quantity 
                       FROM Cocktail_Components WHERE cocktail_id = ?""", (cocktail[0],))
        components = cursor.fetchall()

        print("Состав:")
        for comp in components:
            print(f"- {comp[1]} ({comp[2]})")
    print()
    connect.close()

print("Приложение 'I love drink'\n")
create_tables()

while True:
    print("1 - Добавить ингредиент\n"
          "2 - Добавить коктейль\n"
          "3 - Добавить напиток\n"
          "4 - Продать коктейль\n"
          "5 - Продать напиток\n"
          "6 - Пополнить запасы\n"
          "7 - Показать остатки\n"
          "8 - Показать коктейли\n"
          "9 - Выход")

    action = int(input("Выберите действие: "))

    match action:
        case 1:
            name = input("Введите название ингредиента: ").lower()
            quantity = int(input("Введите кол-во ингредиента: "))
            add_ingredient(name,quantity)
            print("Ингредиент добавлен")

        case 2:
            name = input("Название коктейля: ").lower()
            price = float(input("Цена коктейля: "))
            components = []
            while True:
                print("Добавить компонент:\n"
                      "1 - Алкогольный напиток\n"
                      "2 - Ингредиент\n"
                      "3 - Закончить ввод\n")
                choice = int(input("ввод: "))

                if choice == 1:
                    drink = input("Название напитка: ").lower()
                    volume = float(input("Объем напитка: "))
                    components.append({'type': 'Drink', 'name': drink, 'quantity': volume})
                elif choice == 2:
                    ing = input("Название ингредиента: ").lower()
                    count = float(input("Количество: "))
                    components.append({'type': 'Ingredient', 'name': ing, 'quantity': count})
                elif choice == 3:
                    break
                else:
                    print("Некорректный ввод!")

            add_cocktail(name, price, components)
            print("Коктейль успешно добавлен!")

        case 3:
            name = input("Введите название напитка: ").lower()
            price = float(input("Введите цену за 100 мл напитка: "))
            volume = float(input("Введите начальный объём напитка: "))
            is_alcoholic = input("Напиток алкогольный (+/-) ")
            if is_alcoholic == "+":
                strength = float(input("Введите крепость напитка: "))
                is_alcoholic = True
                add_drink(name,price,is_alcoholic,volume,strength)
                print("Напиток добавлен")
            elif is_alcoholic == "-":
                is_alcoholic = False
                strength = None
                add_drink(name,price,is_alcoholic,volume,strength)
                print("Напиток добавлен")
            else:
                print("Ошибка ввода")

        case 4:
            name = input("Название коктейля для продажи: ").lower()
            sell_cocktail(name)

        case 5:
            name_sell = input("Введите название напитка для продажи: ").lower()
            connect = connect_date_base()
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM Drinks WHERE name = ?",(name_sell,))
            if cursor.fetchone():
                volume_sell = float(input("Введите объём продажи: "))
                cursor.execute("SELECT * FROM Drinks WHERE name = ?", (name_sell,))
                row = cursor.fetchone()
                remains_volume = row[5] - volume_sell
                if remains_volume >= 0:
                    cursor.execute("""UPDATE Drinks SET volume = ?  WHERE name = ?""",
                                   (remains_volume, name_sell))
                    connect.commit()
                else:
                    print("Объём слишком большой")
            else:
                print("Данного напитка нет")

        case 6:
            stocks = int(input("Какие запасы необходимо пополнить (1 - Ингредиенты, 2 - Напитки): "))
            if stocks == 1:
                connect = connect_date_base()
                cursor = connect.cursor()
                ingredient = input("Введите название ингредиента: ")
                cursor.execute("SELECT * FROM Ingredients WHERE name = ?",
                       (ingredient,))
                if cursor.fetchone():
                    ingredient_adding = int(input("Введите кол-во пополнения: "))
                    cursor.execute("""UPDATE Ingredients SET quantity = quantity + ?  WHERE name = ?""",
                           (ingredient_adding, ingredient))
                    connect.commit()
                else:
                    print("Ингредиент не найден")

            elif stocks == 2:
                connect = connect_date_base()
                cursor = connect.cursor()
                drink = input("Введите название напитка: ")
                cursor.execute("SELECT * FROM Drinks WHERE name = ?",
                       (drink,))
                if cursor.fetchone():
                    volume_adding = int(input("Введите объём пополнения: "))
                    cursor.execute("""UPDATE Drinks SET volume = volume + ?  WHERE name = ?""",
                           (volume_adding, drink))
                    connect.commit()
                else:
                    print("Напиток не найден")
            else:
                print("Ошибка ввода")

        case 7:
            connect = connect_date_base()
            cursor = connect.cursor()
            print("Отстатки на складе")
            cursor.execute("SELECT * FROM Drinks")
            all_rows = cursor.fetchall()
            print("Остатки напитков: ")
            for row in all_rows:
                print(f"Название: {row[1]}, Объём остатков: {row[5]} мл")
            cursor.execute("SELECT * FROM Ingredients")
            all_rows = cursor.fetchall()
            print("Остатки ингредиентов: ")
            for row in all_rows:
                print(f"Название: {row[1]}, Кол-во остатков: {row[2]} шт")

        case 8:
            show_cocktails()
        case 9:
            print("Программа завершена")
            break
        case _:
            print("Действие не выбранно")