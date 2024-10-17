from neo4j import GraphDatabase
from pydantic import BaseSettings

class Settings(BaseSettings):
    neo4j_url: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    class Config:
        env_file = ".env"

settings = Settings()

def get_neo4j_driver():
    """Returns the Neo4j driver to be used for database connections."""
    return GraphDatabase.driver(settings.neo4j_url, auth=(settings.neo4j_user, settings.neo4j_password))
