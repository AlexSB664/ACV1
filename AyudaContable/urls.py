"""AyudaContable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
import usuario.views
import superadmin.views
import administrador.views
import usuario.views
#para las fotos
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',usuario.views.login, name='index'),
    url(r'^login/$',usuario.views.login, name='login'),
    url(r'^redi/$',usuario.views.redirecionDeEspacio,name='redi'),
    url(r'^superadmin/index/$',superadmin.views.index0, name='index0'),
    url(r'^superadmin/alta_de_administrador/$',superadmin.views.altaAdmin.as_view(), name='altaAdmin'),
    url(r'^superadmin/alta_de_usuario/$',superadmin.views.altaUsuario.as_view(), name='altaUsuario'),
    url(r'^administrador/index/$',administrador.views.index1,name='index1'),
    url(r'^administrador/subida/$',administrador.views.subidaXML,name='subidaXML'),
    url(r'^administrador/documentos/$',administrador.views.archivosDB, name='vistaDocumentos'),
    url(r'^usuario/index/$',usuario.views.index3,name='index3'),
    url(r'^usuario/documentos/$',usuario.views.archivosGeneral,name='vistaGeneral'),
    url(r'^usuario/documentosN/$',usuario.views.FacturasDelMes,name='vistaN'),
    url(r'^usuario/documentosE/$',usuario.views.leerXMLE,name='vistaE'),
    url(r'^usuario/documentosI/$',usuario.views.leerXMLI,name='vistaI'),
    url(r'^usuario/documentosP/$',usuario.views.leerXMLP,name='vistaP'),
    url(r'^logout$', logout_then_login, name='logout' ),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)