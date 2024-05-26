from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("app find lodging")


def test(request, x):
    return HttpResponse("Hello" + str(x))

