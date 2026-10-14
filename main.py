from DataBase import criar_tabelas
from paciente import cadastrar_paciente, lista_pacientes, buscar_por_cpf
from atendimentos import registrar_atendimento
from relatorios import gerar_relatorio_mensal
from app import AppClinica
        
if __name__ == "__main__":
    app = AppClinica()
    app.mainloop()