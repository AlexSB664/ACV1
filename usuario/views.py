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
from django.db.models import Sum

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
        tabla = serializers.serialize('json',cfdis)
        return HttpResponse(str(tabla))
    else:
        pass

@login_required
def leerXMLN(request):
    tipo = 'N'
    hoy = datetime.date.today()
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id,fecha__month=hoy.month,fecha__year=hoy.year,tipo=tipo)
    total=0
    for cfdi in cfdis:
        total+=cfdi.total
    return render(request,'usuario/documentosDB.html',{'tipo':tipo,'facturas':cfdis,'total':total})

@login_required
def leerXMLI(request):
    tipo = 'I'
    hoy = datetime.date.today()
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id,fecha__month=hoy.month,fecha__year=hoy.year,tipo=tipo)
    total=0
    for cfdi in cfdis:
        total+=cfdi.total
    return render(request,'usuario/documentosDB.html',{'tipo':tipo,'facturas':cfdis,'total':total})

@login_required
def leerXMLE(request):
    tipo = 'E'
    hoy = datetime.date.today()
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id,fecha__month=hoy.month,fecha__year=hoy.year,tipo=tipo)
    total=0
    for cfdi in cfdis:
        total+=cfdi.total
    return render(request,'usuario/documentosDB.html',{'tipo':tipo,'facturas':cfdis,'total':total})

@login_required
def leerXMLP(request):
    tipo = 'P'
    hoy = datetime.date.today()
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id,fecha__month=hoy.month,fecha__year=hoy.year,tipo=tipo)
    total=0
    for cfdi in cfdis:
        total+=cfdi.total
    return render(request,'usuario/documentosDB.html',{'tipo':tipo,'facturas':cfdis,'total':total})

@login_required
def solicitarFactura(request):
    return render(request,'usuario/solicitudFactura.html')

def generarOxxoPay(request):
    import conekta
    conekta.api_key = "key_eYvWV7gSDkNYXsmr"
    conekta.api_version = "2.0.0"
    order = conekta.Order.create({
    "line_items": [{
        "name": "Tacos",
        "unit_price": 10000,
        "quantity": 1
    }],
    #"shipping_lines": [{
    #    "amount": 1500,
    #    "carrier": "FEDEX"
    #}], #shipping_lines - physical goods only
    "currency": "MXN",
    "customer_info": {
      "name": "Fulanito Pérez",
      "email": "fulanito@conekta.com",
      "phone": "+5218181818181"
    },
    "shipping_contact":{
       "address": {
         "street1": "Calle 123, int 2",
         "postal_code": "06100",
         "country": "MX"
       }
    }, #shipping_contact - required only for physical goods
    "charges":[{
      "payment_method": {
        "type": "oxxo_cash"
      }
    }]
    })
    monto=str(order.amount/100)
    referencia=order.charges[0].payment_method.reference
    referencia=referencia[0:4]+"-"+referencia[4:8]+"-"+referencia[8:12]+"-"+referencia[12:14]
    return render(request,'usuario/OxxoPay.html',{'referencia':referencia,'monto':monto})

def webhook(request):
    import json
    mensaje=""
    data = json.loads(HttpRequest.body)
    if data.type == 'charge.paid':
        msg['Subject'] = 'Pago confirmado'
        msg['From'] = me
        msg['To'] = you
        mensaje="exitoso"
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    return render(request,'usuario/OxxoPay.html')
"""    
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
"""