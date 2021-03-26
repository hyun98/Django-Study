from django.shortcuts import render

from django.http import HttpResponse
from .models import Essay, Answer
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import EssayForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


@login_required(login_url='accounts:login')
def essay_modify(request, essay_id):
    """
    게시판 글 수정
    """
    essay = get_object_or_404(Essay, pk=essay_id)
    
    if request.user != essay.author:
        messages.error(request, "수정 권한이 없습니다")
        return redirect('boards:essay_detail', essay_id=essay.id)
    
    if request.method == "POST":
        form = EssayForm(request.POST, instance=essay)
        if form.is_valid():
            essay = form.save(commit=False)
            essay.author = request.user
            # essay.modify_date = timezone.now()
            essay.save()
            return redirect('boards:essay_detail', essay_id=essay.id)
    else:
        form = EssayForm(instance=essay)
    context = {'form': form}
    return render(request, 'pages/board/writeForm.html', context)

@login_required(login_url='accounts:login')
def essay_delete(request, essay_id):
    """ 글 삭제 """
    essay = get_object_or_404(Essay, pk=essay_id)
    
    if request.user != essay.author:
        messages.error(request, "삭제 권한이 없습니다")
        return redirect('boards:essay_detail', essay_id=essay.id)
    essay.delete()
    return redirect('boards:essay_list')
    

@login_required(login_url='accounts:login')
def answer_modify(request, essay_id):
    """
    게시판 댓글 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    
    if request.user != answer.author:
        messages.error(request, "수정 권한이 없습니다")
        return redirect('boards:essay_detail', answer_id=answer.id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            # essay.modify_date = timezone.now()
            answer.save()
            return redirect('boards:essay_detail', essay=essay.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form': form}
    return render(request, 'pages/board/boardDetail.html', context)


@login_required(login_url='accounts:login')
def answer_delete(request, answer_id):
    """ 글 삭제 """
    answer = get_object_or_404(Answer, pk=answer_id)
    
    if request.user != answer.author:
        messages.error(request, "삭제 권한이 없습니다")
        return redirect('boards:essay_detail', answer_id=answer.id)
    answer.delete()
    return redirect('boards:essay_detail', answer.essay.id)



@login_required(login_url='accounts:login')
def like_essay(request, essay_id):
    """글 좋아요 기능"""
    essay = get_object_or_404(Essay, id=essay_id)
    if request.user in essay.like_users.all():
        essay.like_users.remove(request.user)
    else:
        essay.like_users.add(request.user)
    
    return redirect('boards:essay_detail', essay_id=essay.id)