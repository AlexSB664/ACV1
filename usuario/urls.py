from django.conf.urls import *
from usuario import views

urlpatterns = [
	url(r'^$',views.login, name='index'),
	url(r'^login/$',views.login, name='login'),
	url(r'^redi/$',views.redirecionDeEspacio,name='redi'),
	url(r'^usuario/index/$',views.index3,name='index3'),
	url(r'^usuario/documentos/$',views.archivosGeneral,name='vistaGeneral'),
	url(r'^usuario/documentosN/$',views.leerXMLN,name='vistaN'),
	url(r'^usuario/documentosE/$',views.leerXMLE,name='vistaE'),
	url(r'^usuario/documentosI/$',views.leerXMLI,name='vistaI'),
	url(r'^usuario/documentosP/$',views.leerXMLP,name='vistaP'),
	url(r'^usuario/documentosScript/$',views.leerXMLScript,name='vistaScript'),
	url(r'^usuario/firma/$',views.firmaContrato,name='firmaUsuario'),
	url(r'^usuario/firmaCiec/$',views.firmaCiec,name='firmaCiec'),
	url(r'^usuario/solicitar/$',views.solicitarFactura,name='solicitarFactura'),
	url(r'^usuario/referencia/$',views.generarOxxoPay,name='generarReferencia'),
	url(r'^webhook/$',views.webhook,name='webhook'),
]