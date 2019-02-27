from django import forms
from .models import Archivo

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('contador','usuario','archivo',)
        widgets = {
        	'archivo': forms.FileInput(attrs = {'class':'form-control','accept':'.pdf,.xml'}),
        }
        labels = {
			'archivo' : 'Archivo:',
		}

class ArchivoForm1(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ('contador','usuario','archivo',)
        widgets = {
            'archivo': forms.FileInput(attrs = {'class':'form-control','accept':'.pdf,.xml'}),
            'contador': forms.TextInput(attrs = {'class':'form-control','readonly':'readonly'}),
        }
        labels = {
            'archivo' : 'Archivo:',
            'contador': 'Contador:',
        }