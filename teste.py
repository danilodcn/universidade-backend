from requests import *
url = "http://localhost:5000/api/{}/"

d = {
            '_id': '6', 'curso': 'Engenharia Mecânica',
            'nome': 'Edgar Galván', 'numeroAluno': '106', 'tipoAluno': '1'
        }

x = put(url.format("alunos"), data=d)


import ipdb; ipdb.set_trace()