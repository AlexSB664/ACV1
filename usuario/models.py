from django.db import models

# Create your models here.

from superadmin.models import User

class Usuario(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE)
    RFC = models.CharField(max_length=15,null=True)
    tipo_persona = models.CharField(max_length=15,null=True)
    razon_social = models.CharField(max_length=100,null=True,unique=True)
    direccion_fiscal = models.CharField(max_length=125, null=True)
    e_firma = models.FileField(upload_to='profiles',null=True)
    
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
	contador = models.OneToOneField(Usuario, on_delete=models.CASCADE,null=True) 

	def __str__(self):
		return self.RFC.nombre_completo