#MODELS INIT

from sqlalchemy import Column, Integer, String

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from models import Adopter, Adoptions, Animals, Employee, Organization, Supplies, Transfers, Base

engine = create_engine('postgresql://postgres:root@localhost/ShelterHelp', echo=True)

Base.metadata.create_all(engine)
