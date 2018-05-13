#MODELS INIT

from sqlalchemy import Column, Integer, String

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from models import Adopter, Adoptions, Animals, Employee, Organization, Supplies, Transfers, Base, Favorites
from sqlalchemy.orm import Session
import random

engine = create_engine('postgresql://root:root@localhost/ShelterHelp', echo=False)

session = Session(bind=engine)


n = 35


session.add_all([
    Organization (
        "P. Sherman, 42 Wallaby Way, Sydney",
        "555-555-5555",
        random.uniform(0,100),
        "User %d" % i,
        "Sydney Animal Rescue Center",
        "123-_password_-321"
    )
    for i in range(n)
])

session.commit()

session.add_all([
    Adopter (
        "User %d" % i,
        "123-_password_-321",
        "Energetic",
        "A large apartment building",
        13,
        18
    )
    for i in range(n)
])

session.commit()

session.add_all([
    Animals (
        "In good health. Vaccinated, tagged, and spayed/neutered",
        4,
        "Lazy",
        "Garfield",
        "1",
        "static/Garfield.png",
        "Tabby",
        "Cat",
        "Orange",
        "6"
    )
    for i in range(n)
])

session.commit()

session.add_all([
    Employee (
        "User %d" % i,
        "123-_password_-321",
        "1"
    )
    for i in range(n)
])

session.commit()

session.add_all([
    Supplies (
        "Whole grain corn, corn gluten meal, chicken by-product meal, beef fat naturally preserved with mixed-tocopherols, soybean meal, barley, egg and chicken flavor, ground rice, chicken, mono and dicalcium phosphate, poultry and pork digest, calcium carbonate, fish oil, salt, potassium chloride, L-Lysine monohydrochloride, choline chloride, MINERALS [zinc sulfate, ferrous sulfate, manganese sulfate, copper sulfate, calcium iodate, sodium selenite], VITAMINS [Vitamin E supplement, niacin (Vitamin B-3), Vitamin A supplement, calcium pantothenate (Vitamin B-5), pyridoxine hydrochloride (Vitamin B-6), Vitamin B-12 supplement, thiamine mononitrate (Vitamin B-1), Vitamin D-3 supplement, riboflavin supplement (Vitamin B-2), menadione sodium bisulfite complex (Vitamin K), folic acid (Vitamin B-9), biotin (Vitamin B-7)], Yellow 6, Yellow 5, DL-Methionine, Red 40, soybean oil, Blue 2, garlic oil. B-4001",
        "Purina Puppy Chow",
        "30 pounds",
        "Puppy food",
        "1"
    )
    for i in range(n)
])

session.commit()

session.add_all([
    Transfers (
        "1",
        "Outside",
        "In a cage in a padded van",
        "12:00 pm",
        "1",
        "Pending"
    )
    for i in range(n)
])

session.commit()

session.add_all([
    Adoptions ("1","1","Pending")
])

session.commit()

session.add_all([
    Favorites ("1","1")
])

session.commit()

