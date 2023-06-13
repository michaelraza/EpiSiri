from pymongo import MongoClient

# Informations de connexion à MongoDB Atlas
MONGODB_URI = 'mongodb+srv://michaelrazafimandimby:mongodb@cluster0.g8fge2v.mongodb.net/?retryWrites=true&w=majority'

# Fonction pour établir une connexion à la base de données MongoDB
def connect_to_database():
    try:
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database('customerdata')  # Utilisez le nom de votre base de données
        print("Connexion réussie à la base de données MongoDB Atlas")
        return db
    except Exception as e:
        print(f"Impossible de se connecter à la base de données MongoDB Atlas : {str(e)}")

# Connexion à la base de données
db = connect_to_database()
