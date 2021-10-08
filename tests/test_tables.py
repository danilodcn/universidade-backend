from unittest import TestCase
from app.tables import *

class Test_Tables(TestCase):
    def setUp(self) -> None:
        pass

    def teste_cria_com_dict(self):
        d = {
            '_id': '6', 'curso': 'Engenharia Mecânica',
            'nome': 'Edgar Galván', 'numeroAluno': '106', 'tipoAluno': '1'
        }
        aluno = Aluno(d)
        self.assertEqual(aluno.json(), d)
        