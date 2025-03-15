import psycopg2
from config.settings import Settings

def create_tables():
    connection = psycopg2.connect(
        dbname=Settings.DB_NAME,
        user=Settings.DB_USER,
        password=Settings.DB_PASSWORD,
        host=Settings.DB_HOST,
        port=Settings.DB_PORT
    )
    
    cursor = connection.cursor()
    
    #cursor.execute()
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Migrazioni applicate con successo!")

if __name__ == "__main__":
    create_tables()
