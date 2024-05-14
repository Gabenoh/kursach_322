from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Створення об'єкта Base
Base = declarative_base()


# Визначення моделі User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))


# Підключення до бази даних MySQL
engine = create_engine('mysql+mysqlconnector://root:60199@localhost/mysql')

# Створення таблиці за допомогою моделі User
Base.metadata.create_all(engine)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Додавання нового користувача
# new_user = User(username='john_doe', password='password')
# session.add(new_user)
# session.commit()

# # Вибірка користувача за ім'ям
# user = session.query(User).filter_by(username='john_wisky').first()
# print(user.username, user.password)

# Закриття сесії
session.close()
