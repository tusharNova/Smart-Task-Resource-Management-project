from django.shortcuts import render , HttpResponse

from rest_framework import serializers

def Home(request):
    return HttpResponse("<h1>hey user</h1>")
