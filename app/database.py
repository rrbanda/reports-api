# app/database.py

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
DATABASE_NAME = os.getenv("DATABASE_NAME", "patient_db")

# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_session():
    return driver.session(database=DATABASE_NAME)

# Initialize the database
def init_db():
    with get_session() as session:
        # Create constraints if they don't exist
        session.run("""
            CREATE CONSTRAINT IF NOT EXISTS FOR (p:Patient)
            REQUIRE p.study_id IS UNIQUE
        """)

init_db()
