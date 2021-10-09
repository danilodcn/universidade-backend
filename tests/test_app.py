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
        url = self.base_url + "/get/alunos/"
        r = self.app_client.get(url)

        self.assertEqual(r.status_code, 200)

    def test_get_many(self):
        data = {'curso': 'Engenharia ELétrica'}
        url = self.base_url + "/get/alunos/?"
        url += urlencode(data)
        response = self.app_client.get(url, data=data)
        # print(response.json)
        for item in response.json:
            for key, valor in data.items():
                self.assertEqual(item[key], valor)
        # import ipdb; ipdb.set_trace()
    
    def test_put_new_aluno(self):
        url = self.base_url + "/add/alunos/"
        aluno = {
            '_id': '6', 'curso': 'Engenharia Mecânica',
            'nome': 'Edgar Galván', 'numeroAluno': '106', 'tipoAluno': '1'}
        response = self.app_client.put(url, data=aluno)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "Ok")

        # import ipdb; ipdb.set_trace()

    def test_get_all_names(self):
        url = self.base_url + "/allNames"
        print(url)
        response = self.app_client.get(url)
        # import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, 200)