# src/pigua/infrastructure/handlers/dependencies.py

from src.pigua.application.create_pigua import CreatePigua
from src.pigua.infrastructure.adapters.pigua_Mysql import MySQLPiguaRepository
def get_pigua_use_case():
    repo = MySQLPiguaRepository()
    return CreatePigua(repo)
