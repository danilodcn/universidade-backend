from get_data import getData
from tables import Aluno, Disciplina, Turma,HistoricoEscolar, PreRequisito
from db import Banco
import os



possiveis = {
    "cursos": ["Engenharia ELétrica", "Engenharia Mecânica", 
    "Engenharia da Computação", "Ciências da Computação"]
}

DISCIPLINAS = {
    "Introdução a ciências da Computação": "CC",
    "Banco de Dados I": "CC", "Bancos de Dados II": "CC",
    "Cálculo I": "MAT", "Matemática Discreta": "MAT",
    "Introdução a IoT": "CC", "Projeto de Cabeamento Estruturado": "EE",
    "Materiais Elétricos": "EE", "Mecânica Aplicada": "EM"
}
creditos = [2, 3, 4, 5]

__alunos = getData("aluno", 30, **possiveis)
alunos = list(__alunos.get_data())
Alunos = [Aluno(*list(values.values())) for values in alunos]

__disciplina = getData("disciplina", 10, disciplina=DISCIPLINAS, creditos=creditos)
disciplina_ = list(__disciplina.get_data())
Disciplinas = [Disciplina(*list(values.values())) for values in disciplina_]

codigos = [v["numeroDisciplina"] for v in disciplina_]
anos = range(2022-len(codigos), 2022)

__turma = getData("turma", n=1, numeroDisciplina=codigos, ano=anos)
turma = list(__turma.get_data())
Turmas = [Turma(*values.values()) for values in turma]

turmas = [t["_id"] for t in turma]
alunos = [a["numeroAluno"] for a in alunos]

__historico = getData("historico_escolar", numeroAluno=alunos, id_turma=turmas)
historico = list(__historico.get_data())
Historicos = [HistoricoEscolar(*values.values()) for values in historico]

__pre_requisito = getData("pre_requisito", n=2, n_disciplina=codigos)
pre_requisito = list(__pre_requisito.get_data())

PreRequisitos = [PreRequisito(*values.values()) for values in pre_requisito]

password = os.getenv("REDIS_PASSWORD")

client = Banco(password=password)

client.set_many(Alunos + Disciplinas + Turmas + Historicos + PreRequisitos)


import ipdb; ipdb.set_trace()