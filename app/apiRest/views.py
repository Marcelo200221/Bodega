from typing import List
from django.shortcuts import render
from app.kuma.models import Producto

from django.http import JsonResponse
from django.views import View

# Create your views here.


class ObtenerProductos(View):
    def get(self,request):
        productos = Producto.objects.all()
        return JsonResponse(list(productos.values()), safe=False)




