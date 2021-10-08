import os, sys

# import ipdb; ipdb.set_trace()

from flask import Flask, request, jsonify;
try:
    from app.tables import Aluno, Disciplina, Turma, HistoricoEscolar, PreRequisito, Model
    from app.db import Banco
except:
    from tables import Aluno, Disciplina, Turma, HistoricoEscolar, PreRequisito, Model
    from db import Banco


app = Flask(__name__);

password = os.getenv("REDIS_PASSWORD", "senhaPadrao")

print("pass", password)

redis = Banco(password=password)

ROTAS = {
    'alunos': 'Aluno',
    'disciplinas': 'Disciplina',
    'turmas': 'Turmas',
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

@app.get("/")
def home():
    return """
        <div align='center'>
            <h2  font-size=20px height=100px color='red'>
                Essa é uma API!!
            </h2>
        </div>
    """

@app.get('/api/<string:table_name>/')
def get_all(table_name: str):
    table_name = table_name.lower()
    nome_tabela = ROTAS[table_name]
    data = dict(request.values)

    if len(data) == 0:
        retorno = list(redis.search_for_key(f"*{nome_tabela}*", getvalues=True))
    
    else:
        retorno = {data}        
    # print(tabela)
    # import ipdb; ipdb.set_trace()
    return jsonify(retorno)


@app.post("/api/<string:table_name>/")
def get_many(table_name):
    table_name = table_name.lower()
    nome_tabela = ROTAS[table_name]

    tabelas = redis.search_for_key(f"*{nome_tabela}*", getvalues=True)
    import ipdb; ipdb.set_trace()
    


@app.put('/api/<string:table_name>/')
def set_in_db(table_name):
    table_name = table_name.lower()
    nome_tabela = ROTAS[table_name]
    data = dict(request.values)
    print(data)
    # import ipdb; ipdb.set_trace()
        
    # Adicionar novo registo
    ultimo = redis.get_last(nome_tabela, search=None) + 1
    tabela: Model = TABELAS[table_name](data)
    tabela.fields_values[0] = ultimo

    # nome = '{}:{}'.format(tabela.table_name, ultimo)

    response = redis.set_one(tabela)
    status = "Ok" if response else "Error"
    saida = {"status": status}

    return jsonify(saida)



    # return jsonify(tabela)


if __name__ == '__main__':
    from time import sleep
    app.run(debug=True)
