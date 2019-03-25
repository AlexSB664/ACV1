from django.db import models

# Create your models here.
from superadmin.models import User
#from usuario.models import Usuario
import os

def upload_e_firma(self, filename):
    return u'documentos/client_{0}/{1}'.format(self.usuario.id, filename)

class Administrador(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    RFC = models.CharField(max_length=15,null=True)
    numero_de_empleado = models.IntegerField(null=True)
    foto_ine = models.FileField(upload_to='profiles',null=True)
    e_firma_key = models.FileField(upload_to=upload_e_firma,null=True)
    e_firma_cer = models.FileField(upload_to=upload_e_firma,null=True)
    puesto = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return self.email.nombre_completo
    
    class Meta:
        permissions = (
            ('is_admin', 'Is_Admin'),
            ('is_seller', 'Is_Seller'),
            )
