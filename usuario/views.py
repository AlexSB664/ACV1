from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from superadmin.models import User
from usuario.models import Factura, Usuario
from xml.dom import minidom
from django.core import serializers
import datetime
import os
from usuario.forms import FirmaForm, FirmaCiec
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

# Create your views here.
def login(request):
    if  request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('redi')
        else:
            # Show an error page
            mensaje = "Error credenciales no validas"
            return render(request,'login.html',{'mensaje':mensaje})
    else:
        return render(request,'login.html')

@login_required
def firmaContrato(request):
    if request.method == 'POST':
        instance = Usuario.objects.get(email=request.user.id)
        form = FirmaForm(request.POST, request.FILES,instance = instance)
        vacio="entro en POST"
        if form.is_valid():
            instance = form.save(commit=False)
            instance.email = request.user
            instance.save()
            vacio="paso por el form"
            return redirect('index3')
        else:
            pass
    else:
        vacio="entro en nada"
    return render(request,'usuario/index.html',{'vacio':vacio})

@login_required
def firmaCiec(request):
    if request.method == 'POST':
        instance = Usuario.objects.get(email=request.user.id)
        form = FirmaCiec(request.POST, request.FILES,instance = instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.email = request.user
            instance.save()
            return redirect('index3')
        else:
            pass
    else:
        vacio="entro en nada"
    return render(request,'usuario/index.html',{'vacio':vacio})

@login_required
def redirecionDeEspacio(request):
	return render(request,'redirecion.html')

@login_required
def index3(request):
    usuario = User.objects.get(email=request.user.email)
    usuario = Usuario.objects.get(email=usuario.id)
    falta_ciec = None
    firmo = None
    if usuario.e_firma_key == "" and usuario.e_firma_cer == "" and usuario.clave_privada ==  "":
        firmo = False
    else:
        firmo = True
    if firmo and usuario.ciec == "":
        falta_ciec = True
    else:
        falta_ciec = False
    return render(request,'usuario/index.html',{'firmo': firmo,'falta_ciec':falta_ciec})

@login_required
def archivosGeneral(request):
    usuario = User.objects.get(email=request.user.email)
    usuar = Usuario.objects.get(email=usuario.id)
    archivos = Factura.objects.filter(contador=usuar.id)
    return render(request,'usuario/documentosDB.html', {'documentos': archivos})

@login_required
def leerXMLScript(request):
    datos = []
    if request.method == 'GET':
        fecha = request.GET['fecha']
        tipo = request.GET['tipo']
        fecha = datetime.datetime.strptime(fecha,"%Y-%m")
        anio = fecha.year
        mes = fecha.month
        usuar = Usuario.objects.get(email=request.user.id)
        cfdis = Factura.objects.filter(usuario=usuar.id,fecha__month=mes,fecha__year=anio)
        #xmls = clasificar(tipo,cfdis)
        #tabla = entablar(xmls)
        #tabla = filtrarMes(tabla,mes,anio)
        #total = totalDelMes(tabla)
        #for registros in tabla:
        #    datos.append({"RFC": str(registros[1]), 'Nombre': str(registros[2]), 'Fecha':str(registros[3]), 'Vigente':str(registros[4]), 'subtotal':str(registros[5]), 'total':str(registros[6])})
        #tabla = serializers.serialize('json',datos)
        tabla = serializers.serialize('json',cfdis)
        return HttpResponse(str(tabla))
    else:
        pass

def clasificar(tipo,cfdis):
    documentos=[]
    for x in cfdis:
        y=minidom.parse(os.getcwd()+"/media/"+str(x.xml))
        lineas=y.getElementsByTagName("cfdi:Comprobante")
        for linea in lineas:
            z=linea.getAttribute("TipoDeComprobante")
            if z == tipo:
                documentos.append(x)
            else:
                pass
    return documentos

def entablar(xmls):
    tabla = []
    for a in xmls:
        tablatemp = []
        descargartmp = []
        x = a.xml
        descargartmp.append(x)
        y = a.pdf
        descargartmp.append(y)
        tablatemp.append(descargartmp)
        b=minidom.parse(os.getcwd()+"/media/"+str(a.xml))
        lineas = b.getElementsByTagName("cfdi:Receptor")
        c=lineas[0].getAttribute("Rfc")
        d=lineas[0].getAttribute("Nombre")
        tablatemp.append(c)
        tablatemp.append(d)
        lineas2 = b.getElementsByTagName("cfdi:Comprobante")
        e=lineas2[0].getAttribute("Fecha")
        f=lineas2[0].getAttribute("SubTotal")
        g=lineas2[0].getAttribute("Total")
        tablatemp.append(e)
        tablatemp.append("SI")
        tablatemp.append(f)
        tablatemp.append(g)
        tabla.append(tablatemp)
    return tabla

@login_required
def leerXMLN(request):
    tipo = 'N'
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar(tipo,cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total,'tipo':tipo})

@login_required
def leerXMLI(request):
    tipo = 'I'
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar(tipo,cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total,'tipo':tipo})

@login_required
def leerXMLE(request):
    tipo = 'E'
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar(tipo,cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total,'tipo':tipo})

@login_required
def leerXMLP(request):
    tipo = 'P'
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar(tipo,cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total,'tipo':tipo})

def filtrarMes(tabla,mes,anio):
    facturaMes=[]
    for renglon in tabla:
        mesactual=datetime.datetime.strptime(renglon[3],"%Y-%m-%dT%H:%M:%S")
        if  mesactual.month == mes and mesactual.year == anio:
            facturaMes.append(renglon)
        else:
            pass
    return facturaMes

def totalDelMes(tabla):
    total = 0
    for renglon in tabla:
        total+=float(renglon[5])
    return total

def solicitarFactura(request):
    return render(request,'usuario/solicitudFactura.html')