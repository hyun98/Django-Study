from django.urls import path

from . import views

app_name = "boards"

urlpatterns = [
    path('', views.index, name='index'),
    path('essaylist/', views.Essay_list, name='essay_list'),
    path('detail/<int:essay_id>/', views.Essay_detail, name='essay_detail'),
    path('answer/create/<int:essay_id>/', views.answer_create, name='answer_create'),
    path('essay/create/', views.Essay_create, name='essay_create'),
    path('essay/modify/<int:essay_id>/', views.essay_modify, name='essay_modify'),
    path('essay/delete/<int:essay_id>', views.essay_delete, name='essay_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('like/<int:essay_id>/', views.like_essay, name="like_essay"),
    
]
