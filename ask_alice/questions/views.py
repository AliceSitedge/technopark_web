from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator


from .models import Question, Answer


def paginate(data, request, number_on_page):
    paginator = Paginator(data, number_on_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    template = loader.get_template('index.html')

    questions = Question.object.get_fresh()
    questions_on_page = paginate(questions, request, 5)

    context = {
        'questions': questions_on_page
    }
    return HttpResponse(template.render(context, request))


def question(request, question_id):
    template = loader.get_template('question.html')

    question = Question.object.get_question(question_id)
    answers = Answer.object.get_question(question_id)

    context = {
        'question': question,
        'answers': answers
    }
    return HttpResponse(template.render(context, request))


def ask(request):
    template = loader.get_template('ask.html')
    context = {}
    return HttpResponse(template.render(context, request))


def tag(request, tag_name):
    template = loader.get_template('tag.html')

    questions = Question.object.get_tag(tag_name)
    questions_on_page = paginate(questions, request, 5)

    context = {
        'tag_name': tag_name,
        'questions': questions_on_page
    }
    return HttpResponse(template.render(context, request))


def settings(request):
    template = loader.get_template('settings.html')
    context = {
        'nickname': 'AliceSitedge',
        'login': 'alice_sitedge',
        'email': 'a.seledkina@mail.ru'
    }
    return HttpResponse(template.render(context, request))


def signin(request):
    template = loader.get_template('signin.html')
    context = {}
    return HttpResponse(template.render(context, request))


def signup(request):
    template = loader.get_template('signup.html')
    context = {}
    return HttpResponse(template.render(context, request))


def hot(request):
    template = loader.get_template('hot_questions.html')

    questions = Question.object.get_hot()
    questions_on_page = paginate(questions, request, 5)

    context = {
        'questions': questions_on_page
    }
    return HttpResponse(template.render(context, request))
