from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import HttpResponseRedirect


# Create your views here.
def login(request):
    if  request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('redi')
        else:
            # Show an error page
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def redirecionDeEspacio(request):
	return render(request,'redirecion.html')