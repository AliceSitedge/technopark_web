from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from questions.forms import QuestionForm, ProfileForm


from .models import Question, Answer, Profile


def paginate(data, request, number_on_page):
    paginator = Paginator(data, number_on_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    questions = Question.object.get_fresh()
    questions_on_page = paginate(questions, request, 5)

    context = {
        'questions': questions_on_page
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    question = Question.object.get_question(question_id)
    answers = Answer.object.get_question(question_id)
    answers_on_page = paginate(answers, request, 3)

    context = {
        'question': question,
        'answers': answers_on_page
    }
    return render(request, 'question.html', context)


@login_required
def ask(request):
    if request.POST:
        form = QuestionForm(request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', kwargs={'question_id': question.pk}))
        print(form.errors)
    else:
        form = QuestionForm(request.user.profile)

    context = {
        'form': form
    }
    return render(request, 'ask.html', context)


def tag(request, tag_name):
    questions = Question.object.get_tag(tag_name)
    questions_on_page = paginate(questions, request, 5)

    context = {
        'tag_name': tag_name,
        'questions': questions_on_page
    }
    return render(request, 'tag.html', context)


@login_required
def settings(request):
    context = {}
    return render(request, 'settings.html', context)


def signin(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(
            username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_to = request.POST.get('next', 'index')
            return redirect(next_to)
    context = {}
    return render(request, 'signin.html', context)


def signup(request):
    if request.POST:
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save()
            auth.login(request, profile.user)
            next_to = request.POST.get('next', 'index')
            return redirect(next_to)
        print(form.errors)
    else:
        form = ProfileForm()

    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


def signout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def hot(request):
    questions = Question.object.get_hot()
    questions_on_page = paginate(questions, request, 5)

    context = {
        'questions': questions_on_page
    }
    return render(request, 'hot_questions.html', context)
