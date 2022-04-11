from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
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

def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)