from DataBase import conectar

def registrar_atendimento(paciente_id, data, valor_pago, observacao=""):
    with conectar () as conn:
        conn.execute(
            """ INSERT INTO atendimentos (paciente_id, data, valor_pago, observacao)
            
            VALUES (?, ?, ?, ?)""",
           ( paciente_id, data, valor_pago, observacao) 
        )
        conn.commit()
        
def atendimentos_do_mes(ano, mes):
    """Retorna atendimento de um mês específico (mes: 1-12)."""
    prefixo = f"{ano:04d}-{mes:02d}"
    with conectar() as conn:
        return conn.execute("""
            SELECT p.nome, p.cpf, p.celular, a.data, a.valor_pago
            FROM atendimentos a
            JOIN pacientes p ON p.id = a.paciente_id
            WHERE a.data LIKE ?
            ORDER BY a.data
        """, (f"{prefixo}%",)).fetchall()