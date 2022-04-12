from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm

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
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    ctx = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', ctx)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    ctx = {'form': form}
    return render(request, 'pybo/question_form.html', ctx)