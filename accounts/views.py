from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import UserForm

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('boards:index')
    else:
        form = UserForm()
    return render(request, 'pages/reg/register.html', {'form': form})

# @login_required(login_url='common:login')
# def show_profile(request):
#     """ 프로필 보기 """
    
#     return render(request, 'common/profile.html')

def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'pages/404.html', {})