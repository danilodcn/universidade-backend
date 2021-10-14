from django.db import models


class Disciplina(models.Model):
    nome = models.CharField(max_length=60, blank=False, null=False)
    numero_disciplina = models.CharField(max_length=15, blank=False, null=False, unique=True)
    creditos = models.IntegerField(blank=False, null=False)
    departamento = models.CharField(max_length=10, null=False, blank=False)
  

class Turma(models.Model):
    SEMESTRE_CHOICES = [("primeiro", "primeiro"), ("segundo", "segundo")]
    semestre = models.CharField(max_length=15, blank=False, null=False, choices=SEMESTRE_CHOICES)
    ano = models.IntegerField(blank=False, null=False)
    professor = models.CharField(max_length=60, null=False, blank=False)
    id_disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, blank=False, null=False)
    
class Aluno(models.Model):
    TIPO_CHOICES = [
        ("1", "novato"),
        ("2", "segundo ano"),
        ("3", "júnior"),
        ("4", "senior"),
        ("5", "formado"),
    ]

    nome = models.CharField(max_length=50, blank=False, null=False)
    numero = models.IntegerField(blank=False, null=False, unique=True)
    tipo = models.CharField(max_length=1, null=False, blank=False, choices=TIPO_CHOICES)
    id_curso = models.ForeignKey(Disciplina, on_delete=models.CASCADE, blank=False, null=False)


class HistoricoEscolar(models.Model):
    NOTA_CHOICE = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("F", "F"),
    ]
    id_aluno = models.ForeignKey(Aluno, blank=False, null=False, on_delete=models.CASCADE)
    id_turma = models.ForeignKey(Turma, blank=False, null=False, on_delete=models.CASCADE)
    nota = models.CharField(max_length=1, choices=NOTA_CHOICE, blank=False, null=False)


class PreRequisito(models.Model):
    id_disciplina = models.ForeignKey(Disciplina, related_name="disciplina", blank=False, null=False, on_delete=models.CASCADE)
    id_preRequisito = models.ForeignKey(Disciplina, related_name="preRequisito", blank=False, null=False, on_delete=models.CASCADE)