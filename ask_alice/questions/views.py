from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

popular_tags = ['python', 'MySQL', 'django', 'mail.ru', 'technopark', 'yandex.ru']
best_members = ['AliceSitedge', 'AntonyMo', 'LenkaDEA', 'aria_ramm', 'lavender_from_the_valley']


def paginate(data, request, number_on_page):
    paginator = Paginator(data, number_on_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    template = loader.get_template('index.html')
    questions = []
    for i in range(1, 34):
        questions.append({
            'id': i,
            'title': 'How to build a moon park?',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                    'labore et dolore magna aliqua. Nisl tincidunt eget nullam non...',
            'answers': 3,
            'tags': ['black-jack', 'bender']
        })

    questions_on_page = paginate(questions, request, 5)
    print(request.user)
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'questions': questions_on_page
    }
    return HttpResponse(template.render(context, request))


def question(request, question_id):
    template = loader.get_template('question.html')
    question = {
        'title': 'How to build a moon park?',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                'labore et dolore magna aliqua. Nisl tincidunt eget nullam non. Quis hendrerit dolor magna eget '
                'est lorem ipsum dolor sit. Volutpat odio facilisis mauris sit amet massa. Commodo odio aenean '
                'sed adipiscing diam donec adipiscing tristique. Mi eget mauris pharetra et. Non tellus orci ac '
                'auctor augue. Elit at imperdiet dui accumsan sit. Ornare arcu dui vivamus arcu felis. Egestas '
                'integer eget aliquet nibh praesent. In hac habitasse platea dictumst quisque sagittis purus. '
                'Pulvinar elementum integer enim neque volutpat ac.',
        'tags': ['black-jack', 'bender']
    }

    answers = []
    for i in range(1, 4):
        answers.append({
            'text': 'Senectus et netus et malesuada. Nunc pulvinar sapien et ligula ullamcorper malesuada proin. '
                    'Neque convallis a cras semper auctor. Libero id faucibus nisl tincidunt eget. Leo a diam '
                    'sollicitudin tempor id. A lacus vestibulum sed arcu non odio euismod lacinia.',
            'is_correct': True
        })

    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'question_id': question_id,
        'question': question,
        'answers': answers
    }
    return HttpResponse(template.render(context, request))


def ask(request):
    template = loader.get_template('ask.html')
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return HttpResponse(template.render(context, request))


def tag(request, tag_name):
    template = loader.get_template('tag.html')
    questions = []
    for i in range(1, 34):
        questions.append({
            'id': i,
            'title': 'How to build a moon park?',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                    'labore et dolore magna aliqua. Nisl tincidunt eget nullam non...',
            'answers': 3,
            'tags': ['black-jack', 'bender']
        })

    questions_on_page = paginate(questions, request, 5)
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'tag_name': tag_name,
        'questions': questions_on_page
    }
    return HttpResponse(template.render(context, request))


def settings(request):
    template = loader.get_template('settings.html')
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'nickname': 'AliceSitedge', 'login': 'alice_sitedge', 'email': 'a.seledkina@mail.ru'
    }
    return HttpResponse(template.render(context, request))


def signin(request):
    template = loader.get_template('signin.html')
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return HttpResponse(template.render(context, request))


def signup(request):
    template = loader.get_template('signup.html')
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return HttpResponse(template.render(context, request))


def hot(request):
    template = loader.get_template('hot_questions.html')
    questions = []
    for i in range(1, 34):
        questions.append({
            'id': i,
            'title': 'How to build a moon park?',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                    'labore et dolore magna aliqua. Nisl tincidunt eget nullam non...',
            'answers': 3,
            'tags': ['black-jack', 'bender']
        })

    questions_on_page = paginate(questions, request, 5)
    context = {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members,
        'questions': questions_on_page
    }
    return HttpResponse(template.render(context, request))
