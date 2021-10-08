from redis import ResponseError
from tables import Aluno, Curso, Disciplina, HistoricoEscolar, PreRequisito
import os
from db import Banco
from pprint import pprint
import random


os.environ.update(
    {
        "REDIS_PASSWORD": "senhaPadrao",
        "COUNT_PREFIX": "count"
    }
)
password = os.getenv("REDIS_PASSWORD")

client = Banco(password=password)

danilo = Aluno("Danilo", 17, 2, "CC")

curso1 = Curso("Introducao a Computacao", "CC1310", 4, "CC")
curso2 = Curso("Matematica Discreta", "MAT2410", 3, "MATH")

disciplina = Disciplina(85, "MAT2410", "Segundo Semestre", 2021, "Kihg")

hs1 = HistoricoEscolar(17, 112, "B")
hs2 = HistoricoEscolar(17, 119, "C")

n = 50
pr = [PreRequisito("CC3380"+str(random.randint(0, 9)), "CC3320"+str(random.randint(0, 9))) for i in range(n)]
pr_numbers = list(range(1, n+1))

ints = [1, 1, 2, 1, 1, 2] + pr_numbers

client.set_many([danilo, curso1, curso2, disciplina, hs1, hs2, *pr], ints)


# print(client.get_last_number(curso.table_name, False))
keys = client.keys("*")
for key in keys:
    try: 
        print(f"{key} = ", client.hgetall(key))
    except ResponseError:
        try:
            f"{key} = ", client.get(key)
        except ResponseError:
            print("nao deu", key)
            pass

print("\n")
client.del_for_search_term("Cur*1")
x = client.search_for_key("Curso*", True)
pprint(list(x))
