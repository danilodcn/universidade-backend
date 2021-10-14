from django.shortcuts import render
from django.db.models import Model
from django.forms.models import ModelForm
from core.models import Aluno, Disciplina, Turma, PreRequisito, HistoricoEscolar
from web.common.get_attr import get_attr
from web.forms import forms

def cadastrar(request, name: str):
    if request.method == "GET":
        form: ModelForm = get_attr(forms, name.title(), "Form")
        name = "Cadastrar " + name.title()
        print(type(form))
    # import ipdb; ipdb.set_trace()

    return render(request, "web/forms.html", 
        {"form": form, "title": name, "bnt_name": "Cadastrar"}
    )

