from flask import Flask, request, jsonify
from models import db, Potman, Store, Stock, Potion
from flask_cors import CORS

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
        potmen_data = []
        for potman in potmen:
            potman_data = {
                'id': potman.id,
                'name': potman.name,
                'createdAt': potman.created_at,
                'stores': []
            }

            for store in potman.stores:
                store_data = {
                    'id': store.id,
                    'name': store.name,
                    'fame': store.fame,
                    'createdAt': store.created_at,
                    'stokes': []
                }
                potman_data['stores'].append(store_data)

            potmen_data.append(potman_data)
        return jsonify(potmen_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/potman/<int:id>', methods=['GET'])
def get_potman_by_id(id):
    try:
        potman = Potman.query.get(id)

        if potman:
            potman_data = {
                'id': potman.id,
                'name': potman.name,
                'createdAt': potman.created_at,
                'stores': []
            }

            for store in potman.stores:
                store_data = {
                    'id': store.id,
                    'name': store.name,
                    'fame': store.fame,
                    'createdAt': store.created_at,
                    'stokes': []
                }
                potman_data['stores'].append(store_data)

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

        potman_data = {
            'id': new_potman.id,
            'name': new_potman.name,
            'created_at': new_potman.created_at,
            'stores': []
        }

        return jsonify({'message': 'Potman created', 'potman': potman_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# STORES - STORE

@app.route('/stores', methods=['GET'])
def get_stores():
    try:
        stores = Store.query.all()
        stores_data = []
        for store in stores:
            store_data = {
                'id': store.id,
                'name': store.name,
                'createdAt': store.created_at,
                'ownerId': store.owner_id,
                'fame': store.fame,
                'stokes': []
            }

            for stoke in store.stokes:
                stoke_data = {
                    'id': stoke.id,
                    'amount': stoke.amount,
                    'potion_id': stoke.potion_id,
                    'createdAt': stoke.created_at,
                }
                store_data['stokes'].append(stoke_data)

            stores_data.append(store_data)
        return jsonify(stores_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/store/<int:id>', methods=['GET'])
def get_store_by_id(id):
    try:
        store = Store.query.get(id)

        if store:
            store_data = {
                'id': store.id,
                'name': store.name,
                'createdAt': store.created_at,
                'ownerId': store.owner_id,
                'fame': store.fame,
                'stokes': []
            }

            for stoke in store.stokes:
                stoke_data = {
                    'id': stoke.id,
                    'amount': stoke.amount,
                    'potion_id': stoke.potion_id,
                    'createdAt': stoke.created_at,
                }
                store_data['stokes'].append(stoke_data)

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

        store_data = {
            'id': new_store.id,
            'name': new_store.name,
            'fame': new_store.fame,
            'owner_id': new_store.owner_id,
            'created_at': new_store.created_at
        }

        return jsonify({'message': 'Store created', 'store': store_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

# POTIONS - POTION


@app.route('/potions', methods=['GET'])
def get_potions():
    try:
        potions = Potion.query.all()
        potions_data = []
        for potion in potions:
            potion_data = {
                'id': potion.id,
                'name': potion.name,
                'createdAt': potion.created_at,
            }

            potions_data.append(potion_data)
        return jsonify(potions_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/potion/<int:id>', methods=['GET'])
def get_potion_by_id(id):
    try:
        potion = Potion.query.get(id)

        if potion:
            potion_data = {
                'id': potion.id,
                'name': potion.name,
                'createdAt': potion.created_at,
            }

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

        potion_data = {
            'id': new_potion.id,
            'name': new_potion.name,
            'created_at': new_potion.created_at,
        }

        return jsonify({'message': 'Potion created', 'potion': potion_data}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
