from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def login_user(request):
    return HttpResponse('login')

def logout_user(request):
    return HttpResponse('logout')