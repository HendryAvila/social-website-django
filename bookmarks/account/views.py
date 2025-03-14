from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LogingForm, UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

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

@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()

            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})