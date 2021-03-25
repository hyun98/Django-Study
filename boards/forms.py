from django import forms
from boards.models import Essay, Answer


class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content' : '댓글내용'
        }
