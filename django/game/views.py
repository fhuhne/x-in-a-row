from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, World. Let me tell you a story...")
