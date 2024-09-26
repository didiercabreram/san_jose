import pandas as pd
from sqlalchemy import create_engine
import db.db

# Crear el motor de conexión usando SQLAlchemy
engine = create_engine(db.db.connection_string)

# Leer datos en un DataFrame de pandas
def load_data(data):
    return pd.read_sql(data, engine)