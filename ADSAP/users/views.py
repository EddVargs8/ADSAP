from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from users.models import CustomUser as User
from django.views.decorators.cache import never_cache

@never_cache
def custom_login(request):

    if request.user.is_authenticated:
       return redirect(reverse('home:home'))
    
    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')
        
        if not (login_input):
                messages.error(request, "Introduzca un nombre de usuario o un correo electrónico")     
        elif not (password):
                messages.error(request, "Introduzca una contraseña")
        else:
            try:
                if "@" in login_input:
                    user_obj = User.objects.filter(email = login_input).first()
                    user = authenticate(username = user_obj.email, password = password )
                else:
                    user_obj = User.objects.filter(username = login_input).first()
                    user = authenticate(username = user_obj.username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('home:home') 
                else:
                    messages.error(request, "Nombre de usuario o contraseña incorrectos")
            except Exception as e: 
                messages.error(request, "Nombre de usuario o contraseña incorrectos")
                

    return render(request, 'registration/login.html')






