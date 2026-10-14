from DataBase import conectar 

def cadastrar_paciente(nome, cpf, celular):
    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO pacientes (nome, cpf, celular) VALUES (?, ?, ?)", (nome, cpf, celular)
            )
            conn.commit()
            return True, "Paciente cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro: {e}"
                                                                                    
def lista_pacientes():
        with conectar() as conn:
            return conn.execute(
                "SELECT id, nome, cpf, celular FROM pacientes ORDER BY nome"
            ).fetchall()
            
def buscar_por_cpf(cpf):
    with conectar() as conn:
        return conn.execute(
            "SELECT id, nome, cpf, celular FROM pacientes WHERE cpf = ?", (cpf,)
        ).fetchone()