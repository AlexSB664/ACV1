from django.db import models

# Create your models here.

from superadmin.models import User
from usuario.models import Usuario
import os

class Administrador(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    RFC = models.CharField(max_length=15,null=True)
    numero_de_empleado = models.IntegerField(null=True)
    foto_ine = models.FileField(upload_to='profiles',null=True)
    e_firma = models.FileField(upload_to='profiles',null=True)
    puesto = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return self.email.nombre_completo
    
    class Meta:
        permissions = (
            ('is_admin', 'Is_Admin'),
            ('is_seller', 'Is_Seller'),
            )

def upload_to(self, filename):
    return u'documentos/user_{0}/{1}'.format(self.contador.id, filename)

class Factura(models.Model):
    subido_el = models.DateTimeField(auto_now_add=True)
    contador = models.ForeignKey(Administrador, on_delete=models.CASCADE, blank=True, null=True,related_name="contadorACargo")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True,related_name="FDI")
    xml = models.FileField(upload_to=upload_to)
    pdf = models.FileField(upload_to=upload_to)

    def filename(self):
        return os.path.basename(self.xml.name)