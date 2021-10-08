import requests

from typing import List
from random import choices, randint, choice, random
from abc import ABC


def get_nomes(n):
    n = int(n)
    url = "http://www.wjr.eti.br/nameGenerator/index.php"
    o = f"?q={n}&o=json"
    headers = {
        'content-type': 'application/json',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    # import ipdb; ipdb.set_trace()

    r = requests.get(url + o, headers=headers)
    return r.json()


class getData(object):
    escolhas = {}
    data = []
    
    def __init__(self, tipo, n=10, **kwargs) -> None:
        super().__init__()

        self.possibilidades = kwargs
        self.n = n
        self.tipo = tipo

        self.escolhas["aluno"] = self.__aluno
        self.escolhas["disciplina"] = self.__disciplina
        self.escolhas["turma"] = self.__turma
        self.escolhas["historico_escolar"] = self.__historico_escolar
        self.escolhas["pre_requisito"] = self.__pre_requisito
        # import ipdb; ipdb.set_trace()

    def get_data(self):
        return self.escolhas[self.tipo]()

    def __aluno(self):
        retorno = []
        _cursos = self.possibilidades["cursos"]
        fields_names = ["_id", "nome", "numeroAluno", "tipoAluno", "curso"]
        self.nomes = get_nomes(self.n)
        m = 100
        numeros = range(m, m + self.n + 1)
        tipos = [randint(0, 5) for _ in numeros]
        cursos = [choice(_cursos) for _ in numeros]
        iterador = zip(range(self.n), self.nomes, numeros, tipos, cursos)
        
        for valor in iterador:
            new = {}
            for i, campo in enumerate(fields_names):
                new[campo] = valor[i]
            
            yield new
    
    def __disciplina(self):
        __disciplinas = self.possibilidades["disciplina"]
        __creditos = self.possibilidades["creditos"]

        disciplinas = __disciplinas.keys()
        departamentos = __disciplinas.values()
        creditos = [choice(__creditos) for _ in disciplinas]
        numeros = [dep + str(randint(1100, 4500)) for dep in departamentos]
        fields_names = [
        "_id", "nomeDisciplina", "numeroDisciplina", "creditos", "departamento"
        ]
        iterador = zip(range(self.n), disciplinas, numeros, creditos, departamentos)

        for valor in iterador:
            new = dict(zip(fields_names, valor))
            yield new

    def __turma(self):
        numero_disciplina = self.possibilidades["numeroDisciplina"]
        anos = self.possibilidades["ano"]
        n = len(numero_disciplina)
        nomes = get_nomes(n)
        disciplina = 0
        anos = [choice(anos) for _ in numero_disciplina]
        semestre = [choice(["primeiro", "segundo"]) for _ in numero_disciplina]

        fields_names = ["_id", "numeroDisciplina", "semestre", "ano", "professor"]
        iterardor = zip(range(1, n+1), numero_disciplina, semestre, anos, nomes)
        
        for value in iterardor:
            yield dict(zip(fields_names, value))
    
    def __historico_escolar(self):
        numero_aluno = self.possibilidades["numeroAluno"]
        __id_turma = self.possibilidades["id_turma"]
        __notas = "A B C D E F".split(" ")
        # print("Notas = ", __notas)
        alunos = []
        id_turma = []
        notas = []
        for aluno in numero_aluno:
            if random() > .5:
                continue
            else:
                for id in __id_turma:
                    if random() > .5:
                        continue
                    else:
                        alunos.append(aluno)
                        id_turma.append(id)
                        notas.append(choice(__notas))

        fields_names = ["_id", "numeroAluno", "identificadorDisciplina", "nota"]
        iterador = zip(range(len(alunos)), alunos, id_turma, notas)
        for value in iterador:
            yield dict(zip(fields_names, value))

    def __pre_requisito(self):
        numero_disciplina = self.possibilidades["n_disciplina"]
        pre = []
        for id in numero_disciplina:
            pre.append(choice(numero_disciplina))
        
        fields_names = ["_id", "numeroCurso", "numeroDoPreRequisito"]
        iterador = zip(range(len(numero_disciplina)), numero_disciplina, pre)
        for v in iterador:
            yield dict(zip(fields_names, v))