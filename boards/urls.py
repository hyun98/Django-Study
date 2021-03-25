from django.urls import path

from . import views

app_name = "boards"

urlpatterns = [
    path('', views.index, name='index'),
    path('essaylist/', views.Essay_list, name='essay_list'),
    path('<int:essay_id>/', views.Essay_detail, name='essay_detail'),
    path('answer/create/<int:essay_id>/', views.answer_create, name='answer_create'),
    path('essay/create/', views.Essay_create, name='essay_create'),
]
