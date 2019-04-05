from django import forms
from usuario.models import Usuario

class FirmaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('e_firma_key', 'e_firma_cer','clave_privada',)

class FirmaCiec(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('ciec', )