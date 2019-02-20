from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ArchivoForm
# Create your views here.

def index1(request):    
	return render(request,'administrador/index.html')

def subidaXML(request):
	if request.method == 'POST':
		form = ArchivoForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('index1')
	else:
		form = ArchivoForm()
		return render(request, 'administrador/subida.html', {
			'form': form
		})