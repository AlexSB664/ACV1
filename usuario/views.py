from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from superadmin.models import User
from usuario.models import Factura, Usuario
from xml.dom import minidom
import datetime
import os
from usuario.forms import FirmaForm

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
        if cer == "" and key == "":
            vacio="no se capturo los archivos"
        else:
            pass
    else:
        vacio="entro en nada"
    return render(request,'usuario/firma.html',{'vacio':vacio})

def redirecionDeEspacio(request):
	return render(request,'redirecion.html')

def index3(request):
    usuario = User.objects.get(email=request.user.email)
    usuario = Usuario.objects.get(email=usuario.id)
    firmo = None
    if usuario.e_firma_key == "" and usuario.e_firma_cer == "":
        firmo = False
    else:
        firmo = True
    return render(request,'usuario/index.html',{'firmo': firmo})

def archivosGeneral(request):
    usuario = User.objects.get(email=request.user.email)
    usuar = Usuario.objects.get(email=usuario.id)
    archivos = Factura.objects.filter(contador=usuar.id)
    return render(request,'usuario/documentosDB.html', {'documentos': archivos})

def leerXML(request):
    xmlar = minidom.parse(os.getcwd()+"/media/documentos/user_1/EJEMPLO_NOMINA_1.xml")
    lineas = xmlar.getElementsByTagName("cfdi:Comprobante")
    for linea in lineas:
        print(linea.getAttribute("TipoDeComprobante"))
    xmldoc = minidom.parse('synchro.xml')
    readbitlist = xmldoc.getElementsByTagName('readbit')
    values = []
    for s in readbitlist :
        x = s.attributes['bit'].value
        values.append(x)
    return render(request,{'values': values})

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
                break
    return documentos

def entablar(xmls):
    tabla=[]
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

def leerXMLN(request):
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar('N',cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total})

def leerXMLI(request):
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar('I',cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total})

def leerXMLE(request):
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar('E',cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total})

def leerXMLP(request):
    usuar = Usuario.objects.get(email=request.user.id)
    cfdis = Factura.objects.filter(usuario=usuar.id)
    xmls = clasificar('P',cfdis)
    tabla = entablar(xmls)
    hoy = datetime.date.today()
    mes = hoy.month
    anio = hoy.year
    tabla = filtrarMes(tabla,mes,anio)
    total = totalDelMes(tabla)
    return render(request,'usuario/documentosDB.html', {'tabla':tabla,'total':total})

def filtrarMes(tabla,mes,anio):
    facturaMes=[]
    for renglon in tabla:
        mesactual=datetime.datetime.strptime(renglon[3],"%Y-%m-%dT%H:%M:%S")
        if  mesactual.month == mes and mesactual.year == anio:
            facturaMes.append(renglon)
        else:
            break
    return facturaMes

def totalDelMes(tabla):
    total = 0
    for renglon in tabla:
        total+=float(renglon[5])
    return total
