from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


# Create your views here.
def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    ctx = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', ctx)

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    ctx = {'question': question}
    return render(request, 'pybo/question_detail.html', ctx)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    ctx = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', ctx)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    ctx = {'form': form}
    return render(request, 'pybo/question_form.html', ctx)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user != question.author:
        messages.error(request, '?????? ????????? ????????????.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    ctx = {'form': form}
    return render(request, 'pybo/question_form.html', ctx)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user != question.author:
        messages.error(request, '?????? ????????? ????????????.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user != answer.author:
        messages.error(request, '?????? ????????? ????????????.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    ctx = {'form': form, 'answer':answer}
    return render(request, 'pybo/answer_form.html', ctx)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user != answer.author:
        messages.error(request, '?????? ????????? ????????????.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)