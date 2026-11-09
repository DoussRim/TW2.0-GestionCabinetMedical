from django.shortcuts import render
from django.shortcuts import render,redirect

from django.contrib.auth import login
# Create your views here.
def Accueil(request):
    return render(request,"Accueil.html")