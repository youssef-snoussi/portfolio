from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(
                    request,
                    username = cleaned_data['username'],
                    password = cleaned_data['password']
                )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Account not active!')

            else:
                return HttpResponse('Invalid login or password')

    else:
        form = LoginForm()

    return render(request, 'account/forms/login.html', {'form': form})

