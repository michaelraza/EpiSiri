from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://michael_render:myITycl2oBeLOwd9xCC5H2VV05G14wjN@dpg-ci8rn76nqql0lddri59g-a.frankfurt-postgres.render.com/episiri_render'

# Équivalent à une connexion à la base de données
database_engine = create_engine(DATABASE_URL)
# Équivalent à un curseur
SessionTemplate = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)

def get_cursor():
    db = SessionTemplate()
    try:
        yield db
    finally:
        db.close()