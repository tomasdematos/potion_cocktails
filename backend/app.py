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
        return jsonify({'potmen': potmen_data})
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

            return jsonify({'potman': potman_data})
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
            return jsonify({'message': 'Bad request, name not found'}), 400
        new_potman = Potman(name=name)
        db.session.add(new_potman)
        db.session.commit()
        return jsonify({'author': {'name': new_potman.name}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
