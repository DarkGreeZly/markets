from datetime import datetime
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from .models import User, Market, Product
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

pages = Blueprint('pages', __name__)

@pages.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                # session['email'] = request.form['email']
                return redirect(url_for('pages.admin_user'))
            else:
                flash('Incorrect passsword, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)

@pages.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.login'))

@pages.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don`t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('pages.admin_user'))
    else:
        return render_template('signup.html', user=current_user)

@pages.route('market/<id>/createprod', methods=['GET', 'POST'])
@login_required
def create_product(id):
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        img = request.form['img_url']
        description = request.form['description']
        date = datetime.now()
        market_id = id
        if len(title) < 4:
            flash('Title must be at least 5 characters.', category='error')
        elif len(description) < 9:
            flash('Description must be at least 10 characters.', category='error')
        elif len(price) < 1:
            flash('Price cannot be empty.', category='error')
        elif len(img) < 1:
            flash('You must set the image of product.', category='error')
        else:
            product = Product(title=title, price=price, img_url=img, date=date, market_id=market_id, description=description)
            db.session.add(product)
            db.session.commit()
            flash('Product successfully created.', category='success')
            return redirect(url_for('pages.market_page', id=id))

    return render_template('creating_product.html', user=current_user, market_id=id)


@pages.route('/createmarket', methods=['GET', 'POST'])
@login_required
def create_market():
    if request.method == 'POST':
        title = request.form['title']
        address = request.form['address']
        img = request.form['img_url']
        if len(title) < 7:
            flash('Title must be at least 8 characters.', category='error')
        elif len(address) < 19:
            flash('Address must be at least 20 characters.', category='error')
        elif len(img) < 1:
            flash('You must set the image of market.', category='error')
        else:
            market = Market(title=title, address=address, img_url=img)
            db.session.add(market)
            db.session.commit()
            flash('Market successfully created.', category='success')
            return redirect(url_for('pages.admin_user'))

    return render_template('creating_market.html', user=current_user)

@pages.route('/', methods=['GET'])
@login_required
def home_page():
    markets = Market.query.order_by(Market.title).all()
    return render_template('home_page.html', user=current_user, data=markets)

@pages.route('/market/<id>')
@login_required
def market_page(id):
    products = Product.query.filter_by(market_id=id).all()
    print(products)
    cur_market = Market.query.filter_by(id=id).first()
    return render_template('market.html', user=current_user, data=products, current_market=cur_market)

