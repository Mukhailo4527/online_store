import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

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
    product = cursor.execute('''SELECT * FROM goods WHERE LOWER(title)=?''', (title,)).fetchone()
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