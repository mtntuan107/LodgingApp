from rest_framework.serializers import ModelSerializer
from .models import *

class LodgingSerializer(ModelSerializer):
    class Meta:
        model = Lodging
        fields = '__all__'