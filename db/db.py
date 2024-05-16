from sqlalchemy import Column, Integer, String, create_engine, delete, update
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.expression import func

# Створення об'єкта Base
Base = declarative_base()


# Визначення моделі Deck
class Deck(Base):
    __tablename__ = 'deck'
    id = Column(Integer, primary_key=True)
    user = Column(String(255))
    clas = Column(String(255))
    code = Column(String(255))


# Підключення до бази даних MySQL
engine = create_engine('mysql+mysqlconnector://root:60199@localhost/deck')

# Створення таблиці за допомогою моделі Deck
Base.metadata.create_all(engine)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()


def add_deck(user_id, clas, code):
    """Додавання нової колоди"""
    new_deck = Deck(user=user_id, clas=clas, code=code)
    session.add(new_deck)
    session.commit()


def update_deck(row_id, clas, code):
    """Редагування існуючої колоди"""
    stmt = (
        update(Deck)
        .where(Deck.id == row_id)
        .values(clas=clas, code=code)
    )
    # Виконання запиту до бази даних через сесію
    session.execute(stmt)
    session.commit()


def get_random_deck():
    """Отримання випадкової колоди з бази даних"""
    row = session.query(Deck).order_by(func.rand()).first()
    return row.id, row.user, row.clas, row.code


def get_all_deck():
    """Отримання всіх колод з бази даних"""
    deck_list = session.query(Deck).all()
    j = []
    for deck in deck_list:
        j.append((deck.id, deck.user, deck.clas, deck.code))
    return j


def delete_deck(row_id):
    """Видалення рядка з таблиці за індексом"""
    stmt = delete(Deck).where(Deck.id == row_id)
    # Виконання запиту до бази даних через сесію
    session.execute(stmt)
    session.commit()


# Закриття сесії
session.close()
