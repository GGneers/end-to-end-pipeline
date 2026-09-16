import os
from dotenv import load_dotenv
from pymongo import MongoClient
import psycopg
import mysql.connector


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env.creds")

load_dotenv(ENV_FILE, override=True)


# ============================================================
# MONGODB
# ============================================================

def test_mongodb():
    try:
        uri = os.getenv("MongoConnectionString")

        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000
        )

        # MongoDB ping
        client.admin.command("ping")

        client.close()

        print("MongoDB    : ALIVE")

    except Exception as e:
        print(f"MongoDB    : FAILED - {e}")


# ============================================================
# POSTGRESQL
# ============================================================

def test_postgresql():
    try:
        uri = os.getenv("PostgresConnectionString")

        # PostgreSQL connection
        with psycopg.connect(
            uri,
            connect_timeout=5
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        print("PostgreSQL : ALIVE")

    except Exception as e:
        print(f"PostgreSQL : FAILED - {e}")


# ============================================================
# MYSQL
# ============================================================

def test_mysql():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MySQLHost"),
            port=int(os.getenv("MySQLPort")),
            user=os.getenv("MySQLUser"),
            password=os.getenv("MySQLPassword"),
            database=os.getenv("MySQLDatabase"),

            # Aiven requires SSL
            ssl_disabled=False,

            connection_timeout=5
        )

        # MySQL ping
        conn.ping(reconnect=False, attempts=1)

        conn.close()

        print("MySQL      : ALIVE")

    except Exception as e:
        print(f"MySQL      : FAILED - {e}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("       DATABASE CONNECTION TEST")
    print("=" * 50)

    test_mongodb()
    test_postgresql()
    test_mysql()

    print("=" * 50)