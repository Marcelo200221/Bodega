from django.shortcuts import render, redirect, get_object_or_404
from app.kuma.models import Categoria, Producto, Usuario
from .forms import CustomUserCreationForm
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.
def cargarInicio(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "agregar_producto.html", {"prod": productos, "cate": categorias})

def cargarSesion(request):
    return render(request, "registration/login.html")

def cargarAgregarProducto(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "agregar_producto.html", {"prod": productos, "cate": categorias})
    
