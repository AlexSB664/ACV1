from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Contraseña:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','nombre_usuario','password1','password2','nombre_completo','fecha_nacimiento','direccion','genero','foto_perfil')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AdminForm(UserCreationForm):
	RFC = forms.CharField(label='RFC:', widget=forms.TextInput(attrs={'class':'form-control'}))
	numero_de_empleado = forms.CharField(label='Numero de empleado:', widget=forms.TextInput(attrs={'class':'form-control','type': 'number'}))
	foto_ine = forms.FileField(label='Foto o PDF de identificacion:',widget=forms.FileInput(attrs={'class':'form-control'}))
	e_firma = forms.FileField(label='Firma Electronica:',widget=forms.FileInput(attrs={'class':'form-control'}))
	puesto = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=(('Contador Ejecutivo','Contador Ejecutivo'),('Vendedor','Vendedor')),label='Puesto:')
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields
		widgets = {
			'email': forms.EmailInput(attrs = {'class':'form-control'}),
			'nombre_usuario': forms.TextInput(attrs = {'class' : 'form-control'}),
			'password1': forms.PasswordInput(attrs = {'class' : 'form-control'}),
			'nombre_completo': forms.TextInput(attrs = {'class' : 'form-control'}),
			'fecha_nacimiento': forms.DateInput(attrs={'class':'form-control','type': 'date'}),
			'direccion': forms.TextInput(attrs = {'class' : 'form-control'}),
			'genero': forms.Select(attrs = {'class' : 'form-control'},choices=(('Masculino','Masculino'),('Femenino','Femenino'))),
			'foto_perfil': forms.FileInput(attrs = {'class' : 'form-control'}),
		}
		labels = {
			'email' : 'Correo:',
			'nombre_usuario':'Nombre de Usuario:',
			'password1': 'Contraseña',
			'password2': 'Confirmar Contraseña',
			'nombre' : 'Nombre Completo:',
			'fecha_nacimiento' : 'Fecha de Nacimiento:',
			'direccion' : 'Direccion:',
			'genero' : 'Genero:',
			'foto_perfil' : 'Foto de Perfil:',
		}

class UsuarioForm(UserCreationForm):
	RFC = forms.CharField(label='RFC:', widget=forms.TextInput(attrs={'class':'form-control'}))
	tipo_persona = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=(('Persona Fisica','Persona Fisica'),('Persona Moral','Persona Moral')),label='Tipo de Persona:')
	razon_social = forms.CharField(label='Razon Social:', widget=forms.TextInput(attrs={'class':'form-control'}))
	direccion_fiscal = forms.CharField(label='Direccion Fiscal:', widget=forms.TextInput(attrs={'class':'form-control'}))
	e_firma = forms.FileField(label='Firma Electronica:',widget=forms.FileInput(attrs={'class':'form-control'}))
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields
		widgets = {
			'email': forms.EmailInput(attrs = {'class':'form-control'}),
			'nombre_usuario': forms.TextInput(attrs = {'class' : 'form-control'}),
			'password1': forms.PasswordInput(attrs = {'class' : 'form-control'}),
			'nombre_completo': forms.TextInput(attrs = {'class' : 'form-control'}),
			'fecha_nacimiento': forms.DateInput(attrs={'class':'form-control','type': 'date'}),
			'direccion': forms.TextInput(attrs = {'class' : 'form-control'}),
			'genero': forms.Select(attrs = {'class' : 'form-control'},choices=(('Masculino','Masculino'),('Femenino','Femenino'))),
			'foto_perfil': forms.FileInput(attrs = {'class' : 'form-control'}),
		}
		labels = {
			'email' : 'Correo:',
			'nombre_usuario':'Nombre de Usuario:',
			'password1': 'Contraseña',
			'password2': 'Confirmar Contraseña',
			'nombre' : 'Nombre Completo:',
			'fecha_nacimiento' : 'Fecha de Nacimiento:',
			'direccion' : 'Direccion:',
			'genero' : 'Genero:',
			'foto_perfil' : 'Foto de Perfil:',
		}

class LoginForm(forms.ModelForm):
	correo = forms.CharField(label='Correo:',widget=forms.TextInput(attrs={'class':'sr-only'}))
	password = forms.CharField(label='Contraseña:',widget=forms.TextInput(attrs={'class':'sr-only'}))