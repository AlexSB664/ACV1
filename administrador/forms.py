from django import forms
from .models import Archivos

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivos
        fields = ('contador','usuario','archivo',)
        widgets = {
        	'archivo': forms.FileInput(attrs = {'class':'form-control','accept':'.pdf,.xml'}),
        }
        labels = {
			'archivo' : 'Archivo:',
		}