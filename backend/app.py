from flask import Flask, request, jsonify
from models import db, Potman, Store, Stock, Potion
from flask_cors import CORS
from utils import format_potion, format_potions, format_stock, format_stocks, format_stores, format_store, format_potman, format_potmen

app = Flask(__name__)
port = 5000
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/potion_cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def main():
    return 'Making potions'

# POTMEN - POTMAN


@app.route('/potmen', methods=['GET'])
def get_potmen():
    try:
        potmen = Potman.query.all()
        potmen_data = format_potmen(potmen, True)

        return jsonify(potmen_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/potman/<int:id>', methods=['GET'])
def get_potman_by_id(id):
    try:
        potman = Potman.query.get(id)

        if potman:
            potman_data = format_potman(potman)
            return jsonify(potman_data)
        return jsonify({'message': 'Potman not found'}), 404

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/potman', methods=['POST'])
def add_potman():
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({'message': 'Bad request: \'name\' is required'}), 400
        new_potman = Potman(name=name)
        db.session.add(new_potman)
        db.session.commit()

        potman_data = format_potman(new_potman)
        return jsonify({'message': 'Potman created', 'potman': potman_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# STORES - STORE

@app.route('/stores', methods=['GET'])
def get_stores():
    try:
        stores = Store.query.all()
        stores_data = format_stores(stores, True)
        return jsonify(stores_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/store/<int:id>', methods=['GET'])
def get_store_by_id(id):
    try:
        store = Store.query.get(id)

        if store:
            store_data = format_store(store)
            return jsonify(store_data)

        return jsonify({'message': 'Store not found'}), 404

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/store', methods=['POST'])
def add_store():
    try:
        data = request.json
        owner_id = data.get('ownerId')
        name = data.get('name')
        fame = data.get('fame')
        # --------------------------------
        # Check missing fields
        # --------------------------------
        error = ''
        if not name:
            error = error + '\'name\' '
        if not owner_id:
            error = error + '\'ownerId\' '

        if error != '':
            return jsonify({'message': 'Bad request: Missing required fields: ' + error.strip()}), 400
        # --------------------------------
        # Check owner
        # --------------------------------
        owner = Potman.query.get(owner_id)
        if not owner:
            return jsonify({'message': 'Bad request: Invalid owner_id'}), 400
        # --------------------------------

        new_store = Store(name=name, fame=fame, owner_id=owner_id)
        db.session.add(new_store)
        db.session.commit()

        store_data = format_store(new_store)

        return jsonify({'message': 'Store created', 'store': store_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

# POTIONS - POTION


@app.route('/potions', methods=['GET'])
def get_potions():
    try:
        potions = Potion.query.all()
        potions_data = format_potions(potions)
        return jsonify(potions_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/potion/<int:id>', methods=['GET'])
def get_potion_by_id(id):
    try:
        potion = Potion.query.get(id)

        if potion:
            potion_data = format_potion(potion)
            return jsonify(potion_data)

        return jsonify({'message': 'Potion not found'}), 404

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/potion', methods=['POST'])
def add_potion():
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({'message': 'Bad request: \'name\' is required'}), 400
        new_potion = Potion(name=name)
        db.session.add(new_potion)
        db.session.commit()

        potion_data = format_potion(new_potion)

        return jsonify({'message': 'Potion created', 'potion': potion_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

# STOCKS - STOCK


@app.route('/stocks', methods=['GET'])
def get_stocks():
    try:
        stocks = Stock.query.all()
        stocks_data = format_stocks(stocks, True)
        return jsonify(stocks_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/stock/<int:id>', methods=['GET'])
def get_stock_by_id(id):
    try:
        stock = Stock.query.get(id)

        if stock:
            stock_data = format_stock(stock)
            return jsonify(stock_data)

        return jsonify({'message': 'Stock not found'}), 404

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/stock', methods=['POST'])
def add_stock():
    try:
        data = request.json
        store_id = data.get('storeId')
        potion_id = data.get('potionId')
        amount = data.get('amount')
        # --------------------------------
        # Check missing fields
        # --------------------------------
        error = ''
        if not store_id:
            error = error + '\'storeId\' '
        if not potion_id:
            error = error + '\'potionId\' '

        if error != '':
            return jsonify({'message': 'Bad request: Missing required fields: ' + error.strip()}), 400
        # --------------------------------
        # Check Foraints
        # --------------------------------
        store = Store.query.get(store_id)
        if not store:
            return jsonify({'message': 'Bad request: Invalid store_id'}), 400
        potion = Potion.query.get(potion_id)
        if not potion:
            return jsonify({'message': 'Bad request: Invalid potion_id'}), 400
        # --------------------------------
        # Check for existing stock
        # --------------------------------
        stock = Stock.query.filter_by(
            store_id=store_id,
            potion_id=potion_id
        ).first()
        if stock:
            stock_data = format_stock(stock)
            return jsonify({'message': 'Already Existing Stock', 'stock': stock_data}), 200

        new_stock = Stock(
            store_id=store_id,
            potion_id=potion_id,
            amount=amount
        )
        db.session.add(new_stock)
        db.session.commit()

        stock_data = format_stock(new_stock)

        return jsonify({'message': 'Stock created', 'stock': stock_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
