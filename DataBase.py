import os
import sys
import sqlite3
from pathlib import Path

def _pasta_de_dados() -> Path:
    """ 
    Quando roda empacotado (.exe), salva em %APPDATA%/ClinicaCleen.
    Quando roda do código-font, salva na pasta do projeto.
    """
    if getattr(sys, "frozen", False):
      base = Path(os.environ.get("APPDATA", Path.home())) / "ClinicaCleen"
    else:
      base = Path(__file__).resolve().parent
    base.mkdir(parents=True, exist_ok=True)
    return base

nome_banco_de_dados = str(_pasta_de_dados() / 'ClinicaCleen.db')

def conectar(): #definição de conecção de rertorno ao banco de dados 
    return sqlite3.connect(nome_banco_de_dados)

def criar_tabelas():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                celular TEXT NOT NULL
                )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS atendimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                valor_pago REAL NOT NULL,
                observacao TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
                ) 
            """)
        conn.commit()