# votacao/views.py
import io
import base64
import matplotlib.pyplot as plt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Eleitor, Candidato, Voto, Mesario
from .serializers import EleitorSerializer, CandidatoSerializer, VotoSerializer, MesarioSerializer

@api_view(['POST'])
def registrar_mesario(request):
    serializer = MesarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Mesário registrado com sucesso!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cadastrar_eleitor(request):
    serializer = EleitorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Eleitor cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def autorizar_voto(request):
    cpf = request.data.get('cpf')
    try:
        eleitor = Eleitor.objects.get(cpf=cpf)
        if eleitor.ja_votou:
            return Response({"message": "Eleitor já votou!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Eleitor autorizado a votar."}, status=status.HTTP_200_OK)
    except Eleitor.DoesNotExist:
        return Response({"message": "Eleitor não encontrado!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def registrar_voto(request):
    try:
        cpf = request.data['cpf']
        numero_candidato = request.data['numero_candidato']
        
        eleitor = Eleitor.objects.get(cpf=cpf)
        if eleitor.ja_votou:
            return Response({"message": "Eleitor já votou!"}, status=status.HTTP_400_BAD_REQUEST)
        
        candidato = Candidato.objects.get(numero=numero_candidato)
        candidato.votos += 1
        candidato.save()
        
        eleitor.ja_votou = True
        eleitor.save()

        Voto.objects.create(eleitor=eleitor, candidato=candidato)
        
        return Response({"message": "Voto registrado com sucesso!"}, status=status.HTTP_201_CREATED)
    except Eleitor.DoesNotExist:
        return Response({"message": "Eleitor não encontrado!"}, status=status.HTTP_404_NOT_FOUND)
    except Candidato.DoesNotExist:
        return Response({"message": "Candidato não encontrado!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def apuracao(request):
    candidatos = Candidato.objects.all().order_by('-votos')
    serializer = CandidatoSerializer(candidatos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def grafico_eleicoes(request):
    candidatos = Candidato.objects.all()

    nomes = [candidato.nome for candidato in candidatos]
    votos = [candidato.votos for candidato in candidatos]

    # Cria o gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(nomes, votos)
    ax.set_xlabel('Candidatos')
    ax.set_ylabel('Número de Votos')
    ax.set_title('Apuração das Eleições')

    # Salva o gráfico em um buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    # Converte o gráfico para base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Gera o HTML para exibir o gráfico
    html = f"""
    <html>
    <head>
        <title>Resultados das Eleições</title>
    </head>
    <body>
        <h1>Resultados das Eleições</h1>
        <img src='data:image/png;base64,{image_base64}'/>
    </body>
    </html>
    """
    
    return HttpResponse(html)
