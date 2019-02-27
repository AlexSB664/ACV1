from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ArchivoForm1
# Create your views here.

def index1(request):    
	return render(request,'administrador/index.html')

def subidaXML(request):
	if request.method == 'POST':
		form = ArchivoForm1(request.POST, request.FILES)
		if form.is_valid():
			form.save(request.user.id)
			return redirect('index1')
	else:
		form = ArchivoForm1()
		return render(request, 'administrador/subida.html', {
			'form': form
		})