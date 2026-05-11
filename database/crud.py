from database.db import db
from database.models import Client


def create_client(name, number, bouquet, order_count):
    client = Client(
        name=name,
        number=number,
        bouquet=bouquet,
        order_count=order_count
    )

    db.session.add(client)
    db.session.commit()

    return client


def get_all_clients():
    return Client.query.order_by(Client.created_at.desc()).all()


def get_client_by_id(client_id):
    return Client.query.get(client_id)


def delete_client(client_id):
    client = Client.query.get(client_id)

    if client:
        db.session.delete(client)
        db.session.commit()

        return True

    return False