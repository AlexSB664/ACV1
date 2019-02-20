from django.shortcuts import render
from .forms import AdminForm,UsuarioForm
from administrador.models import Administrador
from usuario.models import Usuario
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from django.contrib import auth

# Create your views here.
def index0(request):    
	return render(request,'superadmin/index.html')

class altaAdmin(generic.FormView):
    template_name = 'superadmin/altaAdmin.html'
    form_class = AdminForm
    success_url = reverse_lazy('index0')
    
    def form_valid(self, form):
        Usr = form.save()
        if form.cleaned_data['puesto'] == 'Contador Ejecutivo':
            prm = Permission.objects.get(codename='is_admin')
        if form.cleaned_data['puesto'] == 'Vendedor':
            prm = Permission.objects.get(codename='is_seller')
        Usr.user_permissions.add(prm)
        adminis = Administrador()
        adminis.email = Usr
        adminis.RFC = form.cleaned_data['RFC']
        adminis.numero_de_empleado = form.cleaned_data['numero_de_empleado']
        adminis.foto_ine = form.cleaned_data['foto_ine']
        adminis.e_firma = form.cleaned_data['e_firma']
        adminis.puesto = form.cleaned_data['puesto']
        adminis.save()
        return super(altaAdmin,self).form_valid(form)

class altaUsuario(generic.FormView):
    template_name = 'superadmin/altaUsuario.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('index0')
    
    def form_valid(self, form):
        Usr = form.save()
        prm = Permission.objects.get(codename='is_user')
        Usr.user_permissions.add(prm)
        usuario = Usuario()
        usuario.email = Usr
        usuario.RFC = form.cleaned_data['RFC']
        usuario.tipo_persona = form.cleaned_data['tipo_persona']
        usuario.razon_social = form.cleaned_data['razon_social']
        usuario.direccion_fiscal = form.cleaned_data['direccion_fiscal']
        usuario.e_firma = form.cleaned_data['e_firma']
        usuario.save()
        return super(altaUsuario,self).form_valid(form)

def login(request):
    ctx = {'meh':'meh'}
    if  request.method == 'GET':
        username = request.GET['email']
        password = request.GET['password']
        ctx = {'Alumno': username, 'Padres': password}
        
        user = auth.authenticate(nombre_usuario = email, password = password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/superadmin/index/')
        else:
            # Show an error page
            return render(request, ctx)
    else:
        return render(request, ctx)