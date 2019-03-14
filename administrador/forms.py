from django import forms
from usuario.models import Factura

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ('contador','usuario','xml',)
        widgets = {
        	'xml': forms.FileInput(attrs = {'class':'form-control','accept':'.pdf,.xml'}),
        }
        labels = {
			'xml' : 'Archivo:',
		}

class ArchivoForm1(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ('contador','usuario','xml','pdf')
        widgets = {
            'xml': forms.FileInput(attrs = {'class':'form-control','accept':'.xml'}),
            'pdf': forms.FileInput(attrs = {'class':'form-control','accept':'.pdf'}),
            'contador': forms.TextInput(attrs = {'class':'form-control','readonly':'readonly'}),
        }
        labels = {
            'xml' : 'XML:',
            'pdf':'PDF:',
            'contador': 'Contador:',
        }