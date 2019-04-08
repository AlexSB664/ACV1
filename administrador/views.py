from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from administrador.forms import ArchivoForm1
from administrador.models import Administrador
from usuario.models import Factura
from superadmin.models import User
from django.conf import settings
from usuario.models import Usuario
import os
from django.contrib.auth.decorators import login_required
from xml.dom import minidom
import datetime
# Create your views here.

@login_required
def index1(request):    
	return render(request,'administrador/index.html')

def acomodar(factura):
	lectura= minidom.parse(os.getcwd()+"/media/"+str(factura.xml))
	lineas = lectura.getElementsByTagName("cfdi:Comprobante")
	tipoXML = lineas[0].getAttribute("TipoDeComprobante")
	factura.tipo = tipoXML
	fechaXML = lineas[0].getAttribute("Fecha")
	fechaXML=datetime.datetime.strptime(fechaXML,"%Y-%m-%dT%H:%M:%S")
	factura.fecha = fechaXML
	factura.save()

@login_required
def subidaXML(request):
	if request.method == 'POST':
		form = ArchivoForm1(request.POST, request.FILES)
		if form.is_valid():
			archivo = form.save(commit=False)
			archivo.save()
			acomodar(archivo)
		return redirect('vistaDocumentos')
	else:
		form = ArchivoForm1() 
		usuario = User.objects.get(email=request.user.email)
		admin = Administrador.objects.get(email=usuario.id)
		return render(request, 'administrador/subida.html', {
			'form': form,
			'admin': admin
		})

@login_required
def archivos(request):
	usuario = User.objects.get(email=request.user.email)
	admin = Administrador.objects.get(email=usuario.id)
	url = settings.MEDIA_ROOT
	path=url+"/documentos/user_"+str(admin.id)
	file_list =os.listdir(path)
	return render(request,'administrador/documentos.html', {'documentos': file_list,'url':url})

@login_required
def archivosDB(request):
	usuario = User.objects.get(email=request.user.email)
	admin = Administrador.objects.get(email=usuario.id)
	archivos = Factura.objects.filter(contador=admin.id)
	return render(request,'administrador/documentosDB.html', {'documentos': archivos})

@login_required
def usuariosACargo(request):
	usuario = User.objects.get(email=request.user.email)
	admin = Administrador.objects.get(email=usuario.id)
	usuarios = Usuario.objects.filter(contador=admin.id)
	return render(request,'administrador/usuarios.html',{'usuarios':usuarios})