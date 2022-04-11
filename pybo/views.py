from django.shortcuts import render, get_object_or_404
from .models import Question

# Create your views here.
def index(request):
    question_list = Question.objects.order_by('-create_date')
    ctx = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', ctx)

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    ctx = {'question': question}
    return render(request, 'pybo/question_detail.html', ctx)

