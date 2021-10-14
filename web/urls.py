from django.urls import path
from .views import cadastrar

urlpatterns = [
    path("cadastrar/<name>", cadastrar, name="cadastrar_diarista"),
    # path("listar_diaristas", cadastrar, name="listar_diaristas"),
    # path("editar_diarista/<int:id>", cadastrar, name="editar_diarista"),
    # path("deletar_diarista/<int:id>", cadastrar, name="deletar_diarista")
]