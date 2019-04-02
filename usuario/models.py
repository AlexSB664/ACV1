from django.db import models

# Create your models here.
from superadmin.models import User
from administrador.models import Administrador
import os
from django_cryptography.fields import encrypt

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

class Factura(models.Model):
    subido_el = models.DateTimeField(auto_now_add=True)
    contador = models.ForeignKey(Administrador, on_delete=models.CASCADE, blank=True, null=True,related_name="contadorACargo")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True,related_name="FDI")
    xml = models.FileField(upload_to=upload_to)
    pdf = models.FileField(upload_to=upload_to)

    def filename(self):
        return os.path.basename(self.xml.name)

#    def clean(self):
#        xml = self.cleaned_data.get("xml", False)
#        filetype = magic.from_buffer(xml.read())
#        if not "XML" in filetype:
#            raise ValidationError("File is not XML.")
#        return self.cleaned_data 