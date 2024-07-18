import random

from sqlalchemy.orm import sessionmaker
from models import engine, Employee, City

Session = sessionmaker(bind=engine)
with Session() as session:
    city = session.query(City).filter_by(name='Nova Zagora').first()
    for employee in city.employees:
        print(f"{employee.first_name} {employee.last_name} --> {city.name}")
