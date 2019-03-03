from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from superadmin.models import User
from administrador.models import Archivo
from .models import Usuario
from xml.dom import minidom
import os

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
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def redirecionDeEspacio(request):
	return render(request,'redirecion.html')

def index3(request):    
    return render(request,'usuario/index.html')

def archivosGeneral(request):
    usuario = User.objects.get(email=request.user.email)
    usuar = Usuario.objects.get(email=usuario.id)
    archivos = Archivo.objects.filter(contador=usuar.id)
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

def leerXMLN(request):
    usuario = User.objects.get(email=request.user.email)
    usuar = Usuario.objects.get(email=usuario.id)
    cfdis = Archivo.objects.filter(contador=usuar.id)
    xmls = []
    for cfdi in cfdis:
        x=minidom.parse(os.getcwd()+"/media/"+str(cfdi.archivo))
        lineas=xml.getElementsByTagName("cfdi:Comprobante")
        for linea in lineas:
            y=linea.getAttribute("TipoDeComprobante")
            if y == "N":
                xmls.append(cfdi)
            else:
    return render(request,'usuario/documentosDB.html', {'documentos': archivos})
