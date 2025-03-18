from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from . import forms
from . import models
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def user_login(request):
    if request.method == "POST": #si la solicitud es POST
        form = forms.LogingForm(request.POST) #Instanciamos el formulario con la informacion incluida en el post
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
        form = forms.LogingForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})

def register(request):
    if request.method == "POST":#verificamos que sea un method POST
        user_form = forms.UserRegistrationForm(request.POST) #instanciamos el formulario rellenado con los datos del request
        if user_form.is_valid(): #verificamos
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            models.Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render (request, "account/register.html", {"user_form": user_form})

@login_required
def edit(request) -> render:
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = forms.ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Perfil actualizado '\
                                    'exitosamente!.')
        else:
            messages.error(request, 'Error al actualizar el perfil.')
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})