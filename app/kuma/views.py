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

@login_required
def cargarAgregarProducto(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "agregar_producto.html", {"prod": productos, "cate": categorias})

@login_required
def agregarProducto(request):
    #print("AGREGAR PRODUCTO", request.POST)
    v_sku = request.POST['txtSku']
    v_nombre = request.POST['txtNombre']
    v_descripcion = request.POST['txtDescripcion']
    v_precio = request.POST['txtPrecio']
    v_image = request.FILES.get('txtImg')
    if request.POST['fechaVencimientoSel'] == "":
        v_fecha_vencimiento = None
    else:
        v_fecha_vencimiento = request.POST['fechaVencimientoSel']
    v_stock = request.POST['txtStock']
    v_categoria_id = request.POST.get('cmdCategoria', '')

    if v_sku == ''  or v_nombre == '' or v_descripcion == '' or v_precio == '' or  not v_image or v_stock == '' or v_categoria_id == '':
        messages.warning(request, '.')
        return redirect('/inicio')
    else:
        messages.success(request, '.') #The argument cannot be empty
        v_categoria = Categoria.objects.get(categoria_id = v_categoria_id)
        Producto.objects.create(sku = v_sku, nombre=v_nombre, descripcion=v_descripcion, stock=v_stock, precio=v_precio, fecha_vencimiento=v_fecha_vencimiento,categoria_id=v_categoria, imagen_url=v_image)
    

    

    return redirect('/inicio')
@login_required
def eliminarProducto(request,sku):
    print("ELIMINAR PRODUCTO",sku)
    producto = Producto.objects.get(sku = sku)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(producto.imagen_url))
    os.remove(ruta_imagen)
    producto.delete()
    return redirect('/inicio')

@login_required
def cargarEditarProductos(request, sku):
    productos= Producto.objects.get(sku = sku)
    categorias = Categoria.objects.all()

    cateId = productos.categoria_id

    productoCategoria = Categoria.objects.get(categoria_id = cateId.categoria_id).categoria_id

    return render(request, "editar_producto.html", {"prod": productos, "cate": categorias, "categoriaID": productoCategoria})
@login_required
def editarProductoForm(request):
    v_id = request.POST['txtSku']
    productoBD = Producto.objects.get(sku = v_id)
    v_nombre = request.POST['producto']
    v_descripcion = request.POST['descripcion']
    v_precio = request.POST['precio']
    if request.POST['vencimiento'] == '':
        v_fecha_vencimiento = None
    else:   
        v_fecha_vencimiento = request.POST['vencimiento']
    v_stock = request.POST['stock']
    v_categoria = Categoria.objects.get(categoria_id = request.POST['cmdCategoria'])

    try:
        v_image = request.FILE['imagen']
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(productoBD.imagen_url))
        os.remove(ruta_imagen)
    except:
        v_image = productoBD.imagen_url
    

    productoBD.nombre = v_nombre
    productoBD.descripcion = v_descripcion
    productoBD.stock = v_stock
    productoBD.precio = v_precio
    productoBD.fecha_vencimiento = v_fecha_vencimiento
    productoBD.imagen_url = v_image
    productoBD.categoria_id = v_categoria

    productoBD.save()


    return redirect('/inicio')


def cargarAgregarUsuario(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado existosamente")
            return redirect('/inicio')
        data["form"] = formulario
    return render(request, "registration/registro.html", data)

def agregarUsuario(request):
    v_correo = request.POST['correo']
    v_nombre = request.POST['nombre']
    v_apellido = request.POST['apellido']
    if request.POST['password'] == request.POST['password2'] and request.POST['password'] != '':
        v_contraseña = request.POST['password']
        Usuario.objects.create(correo = v_correo,  nombre=v_nombre, apellido=v_apellido, contraseña=v_contraseña)
    elif request.POST['password'] == '' or request.POST['password2'] == '':
        print("Alguno de los campos de contraseña está vacio")
    else:
        print("Contraseña invalida")

    
    return redirect("/registrar")


    
