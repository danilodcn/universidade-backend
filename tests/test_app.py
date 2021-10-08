from unittest import TestCase

from werkzeug.wrappers import response
from app.app import app
from urllib.parse import urlencode


class TestApp(TestCase):
    def setUp(self) -> None:
        self.app = app
        self.app_client = app.test_client()
        self.app_context = app.app_context()
        self.base_url = "http://localhost:5000/api"

    def test_get_all(self):
        url = self.base_url + "/alunos/"
        r = self.app_client.get(url)

        self.assertEqual(r.status_code, 200)

    def test_get_many(self):
        data = {"id": 2}
        url = self.base_url + "/alunos/?"
        url += urlencode(data)
        response = self.app_client.post(url)
        import ipdb; ipdb.set_trace()
    
    def test_put_new_aluno(self):
        url = self.base_url + "/alunos/"
        aluno = {
            '_id': '6', 'curso': 'Engenharia Mecânica',
            'nome': 'Edgar Galván', 'numeroAluno': '106', 'tipoAluno': '1'}
        response = self.app_client.put(url, data=aluno)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "Ok")

        # import ipdb; ipdb.set_trace()