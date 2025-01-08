from models.database import Base, engine

def initialize_database():
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    initialize_database()
