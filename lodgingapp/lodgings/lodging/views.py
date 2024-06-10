from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


def index(request):
    return HttpResponse("app find lodging")


def test(request, x):
    return HttpResponse("Hello" + str(x))


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(UserSerializer(user).data)


class LodgingViewSet(viewsets.ModelViewSet):
    queryset = Lodging.objects.filter(active=True)
    serializer_class = LodgingSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
