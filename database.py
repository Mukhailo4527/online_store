import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# cursor.execute('''CREATE TABLE users(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 phone TEXT NOT NULL,
#                 email TEXT NOT NULL,
#                 address TEXT NOT NULL,
#                 password TEXT NOT NULL
#                 )''')
#
# cursor.execute('''CREATE TABLE buy_goods(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 category TEXT NOT NULL,
#                 img TEXT NOT NULL,
#                 title TEXT NOT NULL,
#                 desc TEXT NOT NULL,
#                 price REAL NOT NULL,
#                 quantity INTEGER DEFAULT 1
#                 )''')
#
# cursor.execute('''CREATE TABLE goods(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 category TEXT NOT NULL,
#                 img TEXT NOT NULL,
#                 title TEXT NOT NULL,
#                 desc TEXT NOT NULL,
#                 price REAL NOT NULL
#                 )''')
#
# cursor.execute('''CREATE TABLE users_goods(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 category TEXT NOT NULL,
#                 img TEXT NOT NULL,
#                 title TEXT NOT NULL,
#                 desc TEXT NOT NULL,
#                 price REAL NOT NULL,
#                 quantity INTEGER,
#                 email NOT NULL
#                 )''')
#
# conn.commit()
# conn.close()

def add_user(name, phone, email, address, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM users WHERE phone = ?''', (phone,))
    existing_phone = cursor.fetchone()

    if existing_phone:
        conn.close()
        message=f'Користувач з таким номером телефону вже існує'
        return message

    cursor.execute('''SELECT * FROM users WHERE email = ?''', (email,))
    existing_email = cursor.fetchone()

    if existing_email:
        conn.close()
        message=f"Користувач з такою електронною поштою вже існує."
        return message
    cursor.execute('''INSERT INTO users (name, phone, email, address, password) 
                      VALUES (?,?,?,?,?)''', (name, phone, email, address, password))
    conn.commit()
    conn.close()
    return f'Користувача успішно додано'

def get_user_name(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    name = cursor.execute('''SELECT name FROM users WHERE email = ?''', (email,)).fetchone()
    conn.close()
    return name

def get_user(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user_info = cursor.execute('''SELECT * FROM users WHERE email = ?''', (email,)).fetchall()
    conn.close()
    return user_info
def check_login(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    password=cursor.execute('''SELECT password FROM users WHERE email = ?''',(email,)).fetchone()
    conn.close()
    return password[0]

def add_buy_product(category, img, title, desc, price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    existing_item = cursor.execute('''SELECT id, quantity FROM buy_goods WHERE title=?''', (title,)).fetchone()

    if existing_item:
        item_id, quantity = existing_item
        new_quantity = quantity + 1
        cursor.execute('''UPDATE buy_goods SET quantity=? WHERE id=?''', (new_quantity, item_id))
    else:
        cursor.execute('''INSERT INTO buy_goods (category, img, title, desc, price, quantity) 
                          VALUES (?,?,?,?,?,?)''', (category, img, title, desc, price, 1))

    conn.commit()
    conn.close()

def add_product(category, img, title, desc, price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO goods (category, img, title, desc, price) 
            VALUES (?,?,?,?,?)''', (category, img, title, desc, price))
    conn.commit()
    conn.close()

# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()
# cursor.execute('''DELETE FROM goods''')
# conn.commit()
# conn.close()
# Категорія "Смартфони"
# add_product('Смартфони','https://img.freepik.com/free-photo/elegant-smartphone-composition_23-2149437078.jpg?ga=GA1.1.955110324.1723972063&semt=ais_hybrid' , 'iPhone 15', 'iPhone 15 оснащений 6.1-дюймовим дисплеєм Super Retina XDR з яскравими кольорами та чіткими деталями. Він працює на чипі A16 Bionic, який забезпечує швидку продуктивність та енергоефективність. Подвійна камера включає 48-мегапіксельну основну камеру та 12-мегапіксельний ультраширокий об’єктив, що покращує можливості фотографії та відео.', 49999.99)
#
# add_product('Смартфони','data:image/webp;base64,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' , 'Samsung Galaxy S23', 'Samsung Galaxy S23 має 6.2-дюймовий дисплей Dynamic AMOLED, чипсет Exynos 2200 та потрійну камеру, включаючи 64-мегапіксельну основну камеру. Пристрій пропонує 8 ГБ оперативної пам’яті та 128 ГБ внутрішнього сховища.', 45999.99)
#
# add_product('Смартфони','https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSkKtTBiI8yuQyw2yXlqF1DMBlUByoOCpCl3yfZcju_gWmOLPY3QxaIXRX03qwQ8OIr-KlNjy1AQ7lrLPDMw90evhX-HHQXJCYUJGUC6uaIK7BwcO0nTdYnsxgMQVXzR02SDQbNMe_yUA&usqp=CAc' , 'Xiaomi Mi 12', 'Xiaomi Mi 12 оснащений 6.7-дюймовим AMOLED дисплеєм з частотою оновлення 120 Гц, процесором Snapdragon 8 Gen 1 та потрійною камерою на 108 мегапікселів. Підтримується швидка зарядка потужністю 67 Вт.', 39999.99)
#
# # Категорія "Ноутбуки"
# add_product('Ноутбуки','data:image/webp;base64,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' , 'MacBook Pro 14', 'MacBook Pro 14 дюймів працює на чипі M2 Pro, оснащений чудовим дисплеєм Liquid Retina XDR, до 32 ГБ об’єднаної пам’яті та має батарею, що працює до 17 годин.', 99999.99)
#
# add_product('Ноутбуки','https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRK-3YpH3LzyWAPg9gLaakY34ZtIQzWEZZtHzOwWsw85oEAxsNxdAOo5ZB33pBieMDx-M1_y-V6ckQNMYs-x8GueUVGG0Fb2D8ocunB6iaeQI_4M8NVNuAwmQ&usqp=CAc' , 'Dell XPS 13', 'Dell XPS 13 пропонує 13.4-дюймовий FHD+ дисплей, процесор Intel Core i7-1250U, 16 ГБ оперативної пам’яті та SSD на 512 ГБ. Ноутбук компактний, легкий і ідеально підходить для професіоналів, які часто подорожують.', 84999.99)
#
# add_product('Ноутбуки','data:image/webp;base64,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' , 'HP Spectre x360', 'HP Spectre x360 — це 2-в-1 ноутбук з 13.3-дюймовим OLED дисплеєм, процесором Intel Core i7-1165G7, 16 ГБ оперативної пам’яті та SSD на 1 ТБ. Він має стильний дизайн з шарніром на 360 градусів для універсального використання.', 78999.99)
#
# # Категорія "Навушники"
# add_product('Навушники','data:image/webp;base64,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' , 'AirPods Pro', 'AirPods Pro пропонують активне шумозаглушення, режим прозорості та просторовий звук для занурення у аудіо. Вони постачаються з зарядним футляром MagSafe і мають до 24 годин роботи від батареї.', 8999.99)
#
# add_product('Навушники','https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRyvTRmBgchZtQCb7mpNJkd8nxzeB0iRau9lsNUe8-IMw9_GhJV7nUpVyyLXoSGVvlPlTZy07CUHxG1rmiQoSb8tt7aoZMSAx9NIYg5lgs64W06xxN1wBnFamsLknVVDdXv1BnSOmE&usqp=CAc' , 'Sony WH-1000XM5', 'Навушники Sony WH-1000XM5 забезпечують провідне у галузі шумозаглушення, 30 годин роботи від батареї та високу якість звуку високої роздільної здатності. Вони розроблені для комфорту та тривалого прослуховування.', 12999.99)
#
# add_product('Навушники','https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQZzxNk2-pQ3i8QgwfVzSOSmCeyjbZ7FVZ0xZGrfYSjmK_G07oLqX7CI7ip3A4NCXp6zRnRxswu5kEQo5Kv2KBKDENyqhI4fTVnajn3uNzDLp4y1d8XjLKXWDWAUNtAejP0FecqGg&usqp=CAc' , 'Bose QuietComfort 45', 'Bose QuietComfort 45 — це бездротові навушники з активним шумозаглушенням, 24 годинами роботи від батареї та зручним дизайном. Вони ідеально підходять для подорожей і щоденного використання.', 11999.99)
#
# # Категорія "Таблети"
# add_product('Таблети','data:image/webp;base64,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' , 'iPad Pro 12.9', 'iPad Pro 12.9 оснащений дисплеєм Liquid Retina XDR з високою роздільною здатністю, процесором M2 і підтримує Apple Pencil 2-го покоління. Ідеально підходить для професійних дизайнерів і творчих людей.', 79999.99)
#
# add_product('Таблети','data:image/webp;base64,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' , 'Samsung Galaxy Tab S8', 'Samsung Galaxy Tab S8 має 11-дюймовий дисплей LCD, процесор Snapdragon 8 Gen 1 і підтримує S Pen. Добре підходить для роботи та розваг.', 69999.99)
#
# add_product('Таблети','data:image/webp;base64,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' , 'Lenovo Tab P11', 'Lenovo Tab P11 оснащений 11-дюймовим дисплеєм IPS, процесором Qualcomm Snapdragon 750G і підтримує Lenovo Precision Pen 2. Чудовий варіант для перегляду контенту та продуктивної роботи.', 54999.99)


def delete_product(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM goods WHERE id=?''', (id,))
    conn.commit()
    conn.close()

def delete_product_from_orders():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    products = cursor.execute("""DELETE FROM buy_goods """)
    conn.commit()
    conn.close()
    return products


def get_product(title):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    product = cursor.execute('''SELECT * FROM goods WHERE title=?''', (title,)).fetchone()
    conn.close()
    return product

def get_all_products():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    products = cursor.execute('''SELECT * FROM goods''')
    conn.close()
    return products

def want_to_buy_product():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    products = cursor.execute("""SELECT * FROM buy_goods""").fetchall()  # [(1,img,title,..), (2, img,tit...)]
    conn.close()
    return products

def update_product_quantity(product_id, quantity):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE buy_goods SET quantity = ? WHERE id = ?''', (quantity, product_id))
    conn.commit()
    conn.close()

def add_users_goods(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    products = cursor.execute("""SELECT * FROM buy_goods""").fetchall()
    for p in products:
        category=p[1]
        img=p[2]
        title=p[3]
        desc=p[4]
        price=p[5]
        quantity=p[6]
        cursor.execute("""INSERT INTO users_goods (category, img, title, desc, price, quantity, email) VALUES (?,?,?,?,?,?,?)""", (category, img, title, desc, price, quantity, email))
    conn.commit()
    conn.close()