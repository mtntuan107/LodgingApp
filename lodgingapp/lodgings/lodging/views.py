from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *

def index(request):
    return HttpResponse("app find lodging")


def test(request, x):
    return HttpResponse("Hello" + str(x))


class LodgingViewSet(viewsets.ModelViewSet):
    queryset = Lodging.objects.filter(active=True)
    serializer_class = LodgingSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]