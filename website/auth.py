from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Sklad, Tovar, Basket, Order
from . import db
from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from sqlalchemy import func

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if (user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if email == 'admin@gmail.com' and password == '1234':
                    return redirect(url_for('views.adminAddTovar'))
                else:
                    return redirect(url_for('views.catalog'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(nickname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 3 characters.', category='error')
        else:

            new_user = User(email=email, nickname=nickname, password=password2)

            new_user = User(email=email, nickname=nickname, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.catalog'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/AddTovar', methods=['GET', 'POST'])
def add_tovar():
    if request.method == 'POST':
        name = request.form.get('name')
        cost = request.form.get('cost')
        type_of_decoration = request.form.get('type_of_decoration')
        material = request.form.get('material')
        opisanie = request.form.get('opisanie')
        sklad_id = 1
        
        existing_tovar = Tovar.query.filter_by(name=name).first()
        if existing_tovar:
            flash('Tovar already exists.', category='error')
        elif len(name) < 3:
            flash('Name must be greater than 2 characters.', category='error')
        elif len(type_of_decoration) < 11:
            flash('Type_of_decoration must be greater than 11 characters.', category='error')    
        elif not cost or float(cost) < 0:
            flash('Cost must be greater than or equal to 0$.', category='error')   
        elif len(material) < 5:
            flash('color must be greater than 5 characters.', category='error')
        elif len(opisanie) < 10:
            flash('Opisanie must be greater than 10 characters.', category='error')
        else:
            new_tovar = Tovar(name=name, cost=cost, type_of_decoration=type_of_decoration, material=material, opisanie=opisanie, sklad_id=sklad_id)
            db.session.add(new_tovar)
            db.session.commit()
            flash('Tovar added!', category='success')
            return redirect(url_for('views.adminAddTovar'))

    return render_template("AddTovar.html", user=current_user)

@auth.route('/AddSklad', methods=['GET', 'POST'])
def add_sklad():
    if request.method == 'POST':
        street = request.form.get('street')
        existing_sklad = Sklad.query.filter_by(street=street).first()
        if existing_sklad:
            flash('Sklad already exists.', category='error')
        elif len(street) < 3:
            flash('Street must be greater than 2 characters.', category='error')
        else:
            new_sklad = Sklad(street=street)
            db.session.add(new_sklad)
            db.session.commit()
            flash('Sklad added!', category='success')
            return redirect(url_for('views.adminAddSklad'))

    return render_template("AddSklad.html", user=current_user)

@auth.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    if current_user.is_authenticated:
        tovar_name = request.form.get('tovar_name')   
        user_email = current_user.email
        
        
        size = request.form.get('selectedSizeInput')
        quantity = int(request.form.get('count'))
        price1 = float(request.form.get('total_cost'))
        
        price = round(price1*quantity, 2)
        
        existing_item = Basket.query.filter_by(user_email=user_email, tovar_name=tovar_name).first()


        if existing_item:
            existing_item.quantity += quantity
            existing_item.price += float(price)
        else:
            new_item = Basket(user_email=user_email, size=size, tovar_name=tovar_name, quantity=quantity, price=price)
            db.session.add(new_item)

        db.session.commit()

        flash('Tovar added to basket!', category='success')
        return redirect(url_for('views.basket'))
    else:
        flash('Need to authenticate!', category='error')
        return redirect(url_for('views.catalog'))    
    
@auth.route('/basket', methods=['GET', 'POST'])
def createorder():
    if request.method == 'POST':
        max_nomerzakaza = db.session.query(func.max(Order.nomerzakaza)).scalar()
        nomerzakaza = max_nomerzakaza + 1 if max_nomerzakaza is not None else 1
            
        items = Basket.query.filter_by(user_email=current_user.email).all()
        
        basket_price = round(sum(item.price for item in items), 2)
        all_basket_price = basket_price + 5
        
        fio = request.form.get('fio')
        telephone = request.form.get('telephone')
        city = request.form.get('city')
        adress = request.form.get('adress')
        coment = request.form.get('coment')
        promocod = request.form.get('promocod')
          
        if len(fio) < 3:
            flash('FIO must be greater than 3 characters.', category='error')
        elif len(telephone) < 13:
            flash('Telephone must be greater than 13 characters.', category='error')
        elif len(city) < 3:
            flash('City must be greater than 3 characters.', category='error')
        elif len(adress) < 10:
            flash('Adress must be greater than 10 characters.', category='error')
        else:
            basket_items = Basket.query.filter_by(user_email=current_user.email).all()
            for item in basket_items:
                new_order = Order(nomerzakaza=nomerzakaza, 
                                  fio=fio, 
                                  email=current_user.email, 
                                  telephone=telephone, 
                                  city=city, 
                                  adress=adress, 
                                  coment=coment, 
                                  promocod=promocod, 
                                  obsh_price=all_basket_price, 
                                  tovar_size=item.size, 
                                  tovar_name=item.tovar_name, 
                                  tovar_quantity=item.quantity)
                
                db.session.add(new_order)
                db.session.commit()

            flash('Order added!', category='success')
            return redirect(url_for('views.basket'))
    print("------------------", basket_price)
    print("------------------", all_basket_price)
    return render_template("basket.html", user=current_user,  basket_price=basket_price, all_basket_price=all_basket_price)