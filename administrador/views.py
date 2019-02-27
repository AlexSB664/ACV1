from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ArchivoForm1
from .models import Administrador
from superadmin.models import User
# Create your views here.

def index1(request):    
	return render(request,'administrador/index.html')

def subidaXML(request):
	if request.method == 'POST':
		form = ArchivoForm1(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('index1')
	else:
		form = ArchivoForm1() 
		usuario = User.objects.get(email=request.user.email)
		admin = Administrador.objects.get(email=usuario.id)
		return render(request, 'administrador/subida.html', {
			'form': form,
			'admin': admin
		})

def get_id(request):
    current_user = request.user
    return current_user.id