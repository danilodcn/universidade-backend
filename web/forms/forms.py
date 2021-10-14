from django import forms
from django.db.models.base import Model
from core.models import Aluno, Disciplina

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = "__all__"
        

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = "__all__"
    
