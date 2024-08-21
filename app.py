from config import *
app = Flask(__name__)
app.config["SECRET_KEY"] = '111111'

category = None
name = None
currency=float(1.00)

@app.route('/', methods=['GET', 'POST'])
def index():
    global category
    global currency
    global cur
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    products = cursor.execute('''SELECT * FROM goods''').fetchall()
    categorys = cursor.execute('''SELECT DISTINCT category FROM goods''').fetchall()
    conn.close()

    if request.method == 'POST':
        cur=None
        if request.form.get('currency') != None:
            currency = float(request.form.get('currency'))
            print(currency)
            if currency==1.00:
                cur = 'грн'
            if currency==46.05:
                cur = 'EUR'
            if currency==41.35:
                cur = 'USD'
        sort = request.form.get('sort')
        reset_categorys = request.form.get('all_categorys')
        new_category = request.form.get('category')

        if reset_categorys == 'all':
            category = None
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            products = cursor.execute('''SELECT * FROM goods''').fetchall()
            conn.close()
            return redirect('/')

        if new_category:
            category = new_category

        if category:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            products = cursor.execute('''SELECT * FROM goods WHERE category=?''', (category,)).fetchall()
            conn.close()

        return render_template('index.html', products=products, categorys=categorys, name=name, sort=sort, currency=currency, cur=cur)

    return render_template('index.html', products=products, categorys=categorys, name=name, currency=currency)


@app.route('/search')
def search():
    search_result = request.args.get('search')
    return redirect(url_for('buy', title=search_result, name=name))

class UserForm(FlaskForm):
    name = StringField('ПІБ:', validators=[validators.DataRequired(),
                                                   validators.Length(min=10)])
    phone = StringField('Номер телефону:', validators=[validators.DataRequired(),
                                                 validators.Length(min=10, max=13)])
    email = EmailField('Електронна адреса:', validators=[validators.DataRequired(),
                                                          validators.Length(min=11)])
    address = StringField('Адреса доставки:', validators=[validators.DataRequired(),
                                                          validators.Length(min=7)])
    password = PasswordField('Пароль:', validators=[validators.DataRequired(),
                                                          validators.Length(min=5)])

    submit = SubmitField('Зареєструватися')

@app.route('/registr/', methods=['GET','POST'])
def registr():
    form = UserForm()
    if request.method == 'POST':
        message=add_user(name=form.name.data, phone=form.phone.data, email=form.email.data, address=form.address.data, password=form.password.data)
        if message=='Користувача успішно додано':
            return redirect('/login/')
        else:
            return render_template('registr.html', form=form, message=message)
    return render_template('registr.html', form=form, name=name)

@app.route('/login/', methods=['GET','POST'])
def login():
    form = UserForm()
    global email
    email=form.email.data
    if request.method == 'POST':
        if form.password.data == check_login(email):
            add_users_goods(email)
            global name
            name = get_user_name(email)[0]
            return redirect('/cart/')
        else:
            return f'Не правильний email або пароль'
    return render_template('login.html', form=form)

@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    global name
    global email
    global currency
    global cur
    cur=None
    if request.method == 'POST':
        if request.form.get('currency') != None:
            currency = float(request.form.get('currency'))
            if currency==1.00:
                cur = 'грн'
            if currency==46.05:
                cur = 'USD'
            if currency==41.35:
                cur = 'EUR'
        button_value = request.form.get("submit_order")
        if button_value == 'login':
            return redirect('/login/')
        elif button_value == 'order':
            add_users_goods(email)
            delete_product_from_orders()
            return redirect('/')
        for r in request.form:
            if r.startswith('quantity_'):
                product_id = r.split('_')[1]
                quantity = int(request.form[r])
                update_product_quantity(product_id, quantity)
        return redirect('/cart/')
    products = want_to_buy_product()
    if products:
        total_sum=0
        for product in products:
            total_product = product[5]*product[6]
            total_sum+=total_product
        return render_template('cart.html', products=products, total_sum=total_sum, name=name, currency=currency, cur=cur)
    else:
        return render_template('cart.html', message=f'Ваш кошик пустий', name=name)

@app.route('/<title>', methods=["GET", "POST"])
def buy(title):
    product = get_product(title)
    if request.method=='POST':
        add_buy_product(product[1],product[2],product[3],product[4],product[5])
        return redirect('/cart/')
    if product:
        return render_template('buy.html',p=product, name=name)
    else:
        return f'Товар не знайдено'

@app.route('/delete/<int:id>/',methods=['POST'])
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM buy_goods WHERE id=?""",(id,))
    conn.commit()
    conn.close()
    return redirect('/cart/')

@app.route('/profile/<email>/', methods=['GET', "POST"])
def profile(email):
    user_info = get_user(email)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user_products = cursor.execute('''SELECT * FROM users_goods WHERE email=?''',(email,)).fetchall()
    conn.close()
    return render_template('profile.html', products=user_products, user_info=user_info[0])


@app.route('/my_profile/', methods=['GET', "POST"])
def my_profile():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user_products = cursor.execute('''SELECT * FROM users_goods''').fetchall()
    conn.close()
    return render_template('my_profile.html', products=user_products)

if __name__ == '__main__':
    app.run(debug=True)