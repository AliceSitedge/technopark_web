from django.core.paginator import Paginator
from django.shortcuts import render


from .models import Question, Answer


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


def ask(request):
    context = {}
    return render(request, 'ask.html', context)


def tag(request, tag_name):
    questions = Question.object.get_tag(tag_name)
    questions_on_page = paginate(questions, request, 5)

    context = {
        'tag_name': tag_name,
        'questions': questions_on_page
    }
    return render(request, 'tag.html', context)


def settings(request):
    context = {}
    return render(request, 'settings.html', context)


def signin(request):
    context = {}
    return render(request, 'signin.html', context)


def signup(request):
    context = {}
    return render(request, 'signup.html', context)


def hot(request):
    questions = Question.object.get_hot()
    questions_on_page = paginate(questions, request, 5)

    context = {
        'questions': questions_on_page
    }
    return render(request, 'hot_questions.html', context)
