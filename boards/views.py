from django.shortcuts import render

from django.http import HttpResponse
from .models import Essay, Answer
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import EssayForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'pages/main.html')

def Essay_list(request):
    """
    글 목록 출력
    """
    essay_list = Essay.objects.order_by('-create_date')

    context = {'essay_list': essay_list}
    return render(request, 'pages/board/boardList.html', context)

def Essay_detail(request, essay_id):
    """
    질문 내용 출력
    """
    essay = get_object_or_404(Essay, id=essay_id)
    context = {"essay": essay}
    return render(request, 'pages/board/boardDetail.html', context)

# '애너테이션' 이라고 함
# @login_required 애너테이션을 통해 로그인이 되었는지를 우선 검사함
@login_required(login_url='accounts:login')
def answer_create(request, essay_id):
    """ board 답변등록"""
    essay = get_object_or_404(Essay, id=essay_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.essay = essay
            answer.save()
            return redirect('boards:essay_detail', essay_id = essay.id)
    else:
        form = AnswerForm()
    context = {'essay' : essay, 'form' : form}
    return render(request, 'pages/board/boardDetail.html', context)


@login_required(login_url='accounts:login')
def Essay_create(request):
    """ board 질문등록"""
    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save(commit=False)
            essay.author = request.user
            essay.create_date = timezone.now()
            essay.category = "Study"
            essay.save()
            return redirect('boards:essay_list')
    else:
        form = EssayForm()

    context = {'form' : form}
    return render(request, 'pages/board/writeForm.html', context)
