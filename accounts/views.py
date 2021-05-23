from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import *
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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
            profile = Profile()
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('boards:index')
    else:
        form = UserForm()
    return render(request, 'pages/reg/register.html', {'form': form})


def people(request, username): # urls.py에서 넘겨준 인자를 username으로 받는다.
    person = get_object_or_404(get_user_model(), username=username)
    
    return render(request, 'pages/person/profile.html', {'person': person})


@login_required(login_url='accounts:login')
def profile_modify(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('accounts:people', user.username)
        # return redirect('accounts:profile', user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        # 새롭게 추가하는 것이 아니라 수정하는 것이기 때문에
        # 기존의 정보를 가져오기 위해 instance를 지정해야 한다.
        profile, create = Profile.objects.get_or_create(user=request.user)
        # Profile 모델은 User 모델과 1:1 매칭이 되어있지만
        # User 모델에 새로운 인스턴스가 생성된다고 해서 그에 매칭되는 Profile 인스턴스가 생성되는 것은 아니기 때문에
        # 매칭되는 Profile 인스턴스가 있다면 그것을 가져오고, 아니면 새로 생성하도록 한다.
        profile_form = ProfileForm(instance=profile)
        # 아직 profile_modify.html 이 완성되지 않음
        return render(request, 'accounts/profile_modify.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })

def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'pages/404.html')
    

@login_required(login_url='accounts:login')
def follow(request, username):
    # 로그인한 유저 : user
    # 팔로우 대상 유저 : follow_user
    # user = get_object_or_404(get_user_model(), username=request.user.username)
    user = request.user
    print(user.username)
    follow_user = get_object_or_404(get_user_model(), username=username)
    print(follow_user.followers.count())
    print(follow_user.username)
    if user in follow_user.followers.all():
        user.profile.followings.remove(follow_user)
        print("del..")
        # follow_user.followings.remove(user)
    else:
        user.profile.followings.add(follow_user)
        # follow_user.followings.add(user)
    return redirect('accounts:people', username)