from datetime import date
from rest_framework import serializers
from artigo.models import Artigo

# Serializers define the API representation.
class ArtigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artigo
        fields = '__all__'

    def validate_data(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data não pode ser no futuro.")
        return value