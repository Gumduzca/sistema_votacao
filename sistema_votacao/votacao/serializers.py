# votacao/serializers.py
from rest_framework import serializers
from .models import Eleitor, Candidato, Voto, Mesario
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class MesarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Mesario
        fields = ['id', 'nome', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        mesario = Mesario.objects.create(user=user, **validated_data)
        return mesario

class EleitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleitor
        fields = ['id', 'nome', 'cpf', 'ja_votou']

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = ['id', 'nome', 'numero', 'votos']

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['id', 'eleitor', 'candidato', 'data_hora']
