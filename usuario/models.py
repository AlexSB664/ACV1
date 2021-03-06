from django.db import models

# Create your models here.
from superadmin.models import User
from administrador.models import Administrador
import os
from django_cryptography.fields import encrypt
import datetime
import conekta
from datetime import datetime 

def upload_e_firma(self, filename):
    return u'documentos/client_{0}/{1}'.format(self.email.id, filename)

class Usuario(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    RFC = models.CharField(max_length=15,null=True)
    tipo_persona = models.CharField(max_length=15,null=True)
    razon_social = models.CharField(max_length=100,null=True,unique=True)
    direccion_fiscal = models.CharField(max_length=125, null=True)
    e_firma_key = models.FileField(upload_to=upload_e_firma,null=True)
    e_firma_cer = models.FileField(upload_to=upload_e_firma,null=True)
    clave_privada = encrypt(models.CharField(max_length=50))
    ciec = encrypt(models.CharField(max_length=50))
    contador = models.ForeignKey(Administrador, on_delete=models.CASCADE, blank=True, null=True,related_name="contador_personal")    
    def __str__(self):
        return self.email.nombre_completo
    
    class Meta:
        
        permissions = (
            ('is_user', 'Is_User'),
            )

class Cliente(models.Model):
	nombre_completo = models.CharField(max_length=200, null=True)
	razon_social = models.CharField(max_length=200,null=True)
	direccion = models.CharField(max_length=200, null=True)
	RFC = models.CharField(max_length=10,null=True)
	contador =  models.ForeignKey(Usuario,on_delete=models.CASCADE,blank=True, null=True, related_name="cliente_personal")

	def __str__(self):
		return self.RFC.nombre_completo

def upload_to(self, filename):
    return u'documentos/user_{0}/client_{1}/{2}'.format(self.contador.id,self.usuario.id, filename)

def upload_factura(self, filename):
    return u'documentos/user_{0}/client_{1}/{2}{3}-{4}/{5}'.format(self.contador.id,self.usuario.id,self.tipo,self.fecha.year,self.fecha.month, filename)

class Factura(models.Model):
    subido_el = models.DateTimeField(auto_now_add=True)
    contador = models.ForeignKey(Administrador, on_delete=models.CASCADE, blank=True, null=True,related_name="contadorACargo")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True,related_name="FDI")
    xml = models.FileField(upload_to=upload_factura)
    pdf = models.FileField(upload_to=upload_factura)
    fecha = models.DateTimeField(null=True)#format='%Y-%m',input_formats=['%Y-%m'], null=True)
    tipo = models.CharField(max_length=1,null=True)
    RFC = models.CharField(max_length=14,null=True)
    razon_social = models.CharField(max_length=100,null=True)
    vigente = models.BooleanField(default=True)
    sub_total = models.FloatField(null=True)
    total = models.FloatField(null=True)

    def __str__(self):
        return razon_social+str(fecha)

    def filename(self):
        return os.path.basename(self.xml.name)

#    def clean(self):
#        xml = self.cleaned_data.get("xml", False)
#        filetype = magic.from_buffer(xml.read())
#        if not "XML" in filetype:
#            raise ValidationError("File is not XML.")
#        return self.cleaned_data 

class PagoServicio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True,related_name="cargo_a_usuario")
    referencia = models.CharField(max_length=100,null=True)
    id_orden = models.CharField(max_length=22,null=True)
    estado_de_la_orden = models.CharField(max_length=30,null=True)
    monto = models.CharField(max_length=10,null=True)
    fecha_creado = models.DateTimeField(default=datetime.now, blank=True)

    
    def __str__(self):
        return str(self.referencia)