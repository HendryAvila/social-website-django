from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LogingForm

def user_login(request):
    if request.method == "POST": #si la solicitud es POST
        form = LogingForm(request.POST) #Instanciamos el formulario con la informacion incluida en el post
        if form.is_valid(): #verifo que los datos pasados son correctos
            cd = form.cleaned_data #limpia los datos y devuelve un diccionario
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
            if user is not None: #verificamos que el user no devuelve None, es decir que paso la authenticacion
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated')
                else:
                    return HttpResponse('Disable account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LogingForm()
    return render(request, 'account/login.html', {'form': form})