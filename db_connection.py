
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


url = URL.create(
    drivername="postgresql",
    host="172.17.0.2",
    username="postgres",
    password="pass",
    port=5432,
    database="padel"
)

engine = create_engine(url)
db_connection = engine.connect()