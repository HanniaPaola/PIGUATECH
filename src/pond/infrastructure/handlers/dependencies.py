# src/pond/infrastructure/handlers/dependencies.py
from src.pond.application.create_pond import CreatePond
from src.pond.infrastructure.adapters.pond_Mysql import MySQLPondRepository

def get_pond_use_case():
    repo = MySQLPondRepository()
    return CreatePond(repo)