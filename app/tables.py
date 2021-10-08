from abc import ABC


class Model(ABC):
    table_name = ""
    fields_names = []
    def __init__(self, *fields_values):
        # self.field_name = field_name
        self.fields_names = ["_id"] + self.fields_names 
        if isinstance(fields_values[0], dict):
            fields_values = [fields_values[0][key] for key in self.fields_names]
        
        # import ipdb; ipdb.set_trace()

        self.fields_values = fields_values
    
    def config_data(self):
        iterator = zip(self.fields_names, self.fields_values)

        self.data = {key: value for key, value in iterator}

    def json(self):
        return dict(zip(self.fields_names, self.fields_values))

    def get_data(self):
        self.config_data()
        id = self.data["_id"]
        field = "{}:{}".format(self.table_name, id)
        for key, value in self.data.items():
            yield field, key, value

    def __repr__ (self) -> str:
        return str(self.json())

class Aluno(Model):
    table_name = "Aluno"
    fields_names = ["nome", "numeroAluno", "tipoAluno", "curso"]

class Disciplina(Model):
    table_name = "Disciplina"
    fields_names = [
        "nomeDisciplina", "numeroDisciplina", "creditos", "departamento"
        ] 

class Turma(Model):
    table_name = "Turma"
    fields_names = ["numeroDisciplina", "semestre", "ano", "professor"]

class HistoricoEscolar(Model):
    table_name = "HistoricoEscolar"
    fields_names = ["numeroAluno", "identificadorDisciplina", "nota"]

class PreRequisito(Model):
    table_name = "PreRequisito"
    fields_names = ["numeroCurso", "numeroDoPreRequisito"]
    