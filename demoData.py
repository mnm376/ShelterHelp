#MODELS INIT

from sqlalchemy import Column, Integer, String

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models import Adopter, Adoptions, Animals, Employee, Organization, Supplies, Transfers, Base, Favorites
from sqlalchemy.orm import Session
import random

engine = create_engine('postgresql://postgres:root@localhost/ShelterHelp', echo=False)

session = Session(bind=engine)

personalityList = ['Lazy', 'Energetic', 'Shy']

session.add_all([
    Organization (
        "P. Sherman, 42 Wallaby Way, Sydney",
        "555-555-5555",
        44,
        "User",
        "Sydney Animal Rescue Center",
        "password",
        100
    ),
    Organization (
        "P. Sherman, 42 Wallaby Way, Sydney",
        "666-666-6666",
        27,
        "Admin",
        "NYC Shelter Manhattan"
        "123",
        100
    ),
    Organization (
        "P. Sherman, 42 Wallaby Way, Sydney",
        "777-777-7777",
        27,
        "First",
        "Sydney Animal Rescue Center",
        "abc",
        100
    )
])

session.commit()
for i in range(4):
    session.add_all([
        Animals (
            "In good health. Vaccinated, tagged, and spayed/neutered",
            random.uniform(1,10),
            personalityList[int(random.uniform(0,3))],
            "Garfield",
            1,
            "static/Garfield.png",
            "Tabby",
            "Cat",
            "Orange",
            "Large"
        )
    ])
    session.commit()

session.add_all([
    Employee (
        "Superuser",
        "123",
        "1"
    )
])

session.commit()

session.add_all([
    Supplies (
        "Whole grain corn",
        "Purina Puppy Chow",
        "30 pounds",
        "Puppy food",
        "1"
    )
])

session.commit()

