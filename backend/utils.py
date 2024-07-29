from models import db, Potman, Store, Stock, Potion


def format_potion(potion):
    potion_data = {
        'id': potion.id,
        'name': potion.name,
        'createdAt': potion.created_at,
    }
    return potion_data


def format_potions(potions):
    potions_data = []
    for potion in potions:
        potion_data = format_potion(potion)
        potions_data.append(potion_data)

    return potions_data


def format_stock(stock, simple=False):
    stock_data = {
        'id': stock.id,
        'amount': stock.amount,
        'potion_id': stock.potion_id,
        'createdAt': stock.created_at
    }

    if not simple:
        potion = Potion.query.get(stock.potion_id)
        potion_data = format_potion(potion)
        stock_data['potion'] = potion_data

    return stock_data


def format_stocks(stocks, simple=False):
    stocks_data = []

    for stock in stocks:
        stock_data = format_stock(stock, simple)
        stocks_data.append(stock_data)

    return stocks_data


def format_store(store, simple=False):
    store_data = {
        'id': store.id,
        'name': store.name,
        'createdAt': store.created_at,
        'ownerId': store.owner_id,
        'fame': store.fame,
        'stocks': format_stocks(store.stocks, simple)
    }
    return store_data


def format_stores(stores, simple=False):
    stores_data = []
    for store in stores:
        store_data = format_store(store, simple)
        stores_data.append(store_data)

    return stores_data


def format_potman(potman, simple=False):
    potman_data = {
        'id': potman.id,
        'name': potman.name,
        'createdAt': potman.created_at,
        'stores': format_stores(potman.stores, simple),
    }
    return potman_data


def format_potmen(potmen, simple=False):
    potmen_data = []
    for potman in potmen:
        potman_data = format_potman(potman, simple)
        potmen_data.append(potman_data)
    return potmen_data
