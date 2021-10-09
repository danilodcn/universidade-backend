import os, sys

# import ipdb; ipdb.set_trace()

from flask import Flask, request, jsonify;
from flask_cors import CORS
try:
    from app.tables import Aluno, Disciplina, Turma, HistoricoEscolar, PreRequisito, Model
    from app.db import Banco
except:
    from tables import Aluno, Disciplina, Turma, HistoricoEscolar, PreRequisito, Model
    from db import Banco


app = Flask(__name__);
CORS(app)

password = os.getenv("REDIS_PASSWORD", "senhaPadrao")

print("pass", password)

redis = Banco(password=password)

ROTAS = {
    'alunos': 'Aluno',
    'disciplinas': 'Disciplina',
    'turmas': 'Turma',
    'historicos': 'HistoricoEscolar',
    'pre-requisitos': 'PreRequisito'
}

TABELAS = {
    'alunos': Aluno,
    'disciplinas': Disciplina,
    'turmas': Turma,
    'historicos': HistoricoEscolar,
    'pre-requisitos': PreRequisito
}


def busca_por_items(termos_busca: dict, dicionarios: list):

    def busca_item(nome, valor):
        r = []
        for dic in dicionarios:
            try:
                if dic[nome] == valor:
                    # import ipdb; ipdb.set_trace()
                    r.append(dic)
            except KeyError:
                continue
        return r

    # import ipdb; ipdb.set_trace()
    for key, valor in termos_busca.items():
        retorno = []
        item = busca_item(key, valor)
        if item != None:
            retorno.extend(item)
        
        dicionarios = retorno
        if dicionarios == {}: 
            return []
    
    return dicionarios


@app.get("/")
def home():
    return """
        <div align='center'>
            <h2  font-size=20px height=100px color='red'>
                Essa é uma API!!
            </h2>
        </div>
    """

@app.get("/api/allNames")
def all_names():
    # import ipdb; ipdb.set_trace()
    return jsonify(list(TABELAS.keys()))

@app.get('/api/get/<string:table_name>/')
def get_all(table_name: str):
    table_name = table_name.lower()
    nome_tabela = ROTAS[table_name]
    data = request.values.to_dict()
    items = redis.search_for_key(f"*{nome_tabela}*", getvalues=True)

    dicionarios = []
    for item in items:
        dicionarios += list(item.values())

    # import ipdb; ipdb.set_trace()
    if len(data) == 0:
        retorno = dicionarios
    
    else:
        retorno = busca_por_items(data, dicionarios)
        # import ipdb; ipdb.set_trace()
             
    # print(tabela)
    return jsonify(retorno)
    


@app.put('/api/add/<string:table_name>/')
def set_in_db(table_name):
    table_name = table_name.lower()
    nome_tabela = ROTAS[table_name]
    data = dict(request.values)
    # import ipdb; ipdb.set_trace()
        
    # Adicionar novo registo
    ultimo = redis.get_last(nome_tabela, search=None) + 1
    tabela: Model = TABELAS[table_name](data)
    tabela.fields_values[0] = ultimo

    response = redis.set_one(tabela)
    status = "Ok" if response else "Error"
    saida = {"status": status}

    return jsonify(saida)


if __name__ == '__main__':
    from time import sleep
    app.run(debug=True)
