from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Tovar, Basket, Order
from . import db
import json
from collections import defaultdict
from sqlalchemy import func

views = Blueprint('views', __name__)

@views.route('/')
def catalog():
    tovar_list = Tovar.query.all()
    return render_template('catalog.html', tovar_list=tovar_list, user=current_user)

@views.route('/AddTovar')
def adminAddTovar():
    return render_template('AddTovar.html', user=current_user)

@views.route('/AddSklad')
def adminAddSklad():
    return render_template('AddSklad.html', user=current_user)

@views.route('/product/<name>')
def product(name):
    tovar = Tovar.query.filter_by(name=name).first()
    if tovar is None:
        return render_template('error.html'), 404
    return render_template('product.html', tovar=tovar, user=current_user)

@views.route('/basket')
@login_required
def basket():
    user_email = current_user.email
    items = Basket.query.filter_by(user_email=user_email).all()
    
    basket_price = round(sum(item.price for item in items), 2)
    all_basket_price = basket_price + 5
    
    return render_template('basket.html', items=items, user=current_user, basket_price=basket_price, all_basket_price=all_basket_price)

@views.route('/remove_item', methods=['POST'])
@login_required
def remove_item():
    data = json.loads(request.data)
    id = data['id']
    
    item = Basket.query.get(id)
    
    if item:
        if item.user_email == current_user.email:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Товар удален из корзины"})
        else:
            return jsonify({"error": "Вы не можете удалить этот товар"})
    else:
        return jsonify({"error": "Товар не найден"})  
    
@views.route('/myOrders')
@login_required
def myOrders():
    orders = Order.query.filter_by(email=current_user.email).all()
    order_dict = defaultdict(list)
    order_prices = {}

    for order in orders:
        order_dict[order.nomerzakaza].append(order)
        if order.nomerzakaza not in order_prices:
            first_order = Order.query.filter_by(nomerzakaza=order.nomerzakaza).first()
            order_prices[order.nomerzakaza] = first_order.obsh_price
    return render_template('myOrders.html', order_dict=order_dict, user=current_user, order_prices=order_prices)