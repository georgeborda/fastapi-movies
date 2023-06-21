import os
# Poder interactuar con el sistema operativo
from sqlalchemy import create_engine
# Poder crear el motor
from sqlalchemy.orm.session import sessionmaker
# Poder crear la sesión
from sqlalchemy.ext.declarative import declarative_base
# Poder manipular las tablas de la base de datos


sqlite_file_name = "../database.sqlite"
# Creamos una variable con el nombre de la base de datos, se va a crear en el directorio principal y no en el de config

base_dir = os.path.dirname(os.path.realpath(__file__))
# Acá estamos leyendo el path donde se encuentra este archivo (file)

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
# Creamos la url de la base de datos, de esta manera nos conectemos a la base de datos

engine = create_engine(database_url, echo=True)
# Creamos el motor, le pasamos la url de la base de datos, y ponemos echo= True para que al momento de crear la base de datos nos muestre el código

Session = sessionmaker(bind=engine)
# Creamos una sesión para conectarnos a la base de datos

Base = declarative_base()