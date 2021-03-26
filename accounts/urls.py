from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path('signup/', views.signup, name='signup'),
    path('/<str:username>/', views.people, name="people"),
    path('profile_modify/<str:username>', views.profile_modify, name="profile_modify"),
    path('<str:username>/follow/', views.follow, name="follow"),
]