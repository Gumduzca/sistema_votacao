# votacao/urls.py
from django.urls import path
from .views import (
    registrar_mesario, cadastrar_eleitor,
    autorizar_voto, registrar_voto,
    apuracao, grafico_eleicoes
)

urlpatterns = [
    path('mesario/registrar/', registrar_mesario, name='registrar_mesario'),
    path('mesario/cadastrar-eleitor/', cadastrar_eleitor, name='cadastrar_eleitor'),
    path('mesario/autorizar/', autorizar_voto, name='autorizar_voto'),
    path('urna/registrar/', registrar_voto, name='registrar_voto'),
    path('apuracao/', apuracao, name='apuracao'),
    path('grafico-eleicoes/', grafico_eleicoes, name='grafico_eleicoes'),
]
