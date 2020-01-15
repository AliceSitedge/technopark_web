from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from random import randint
from random import choice

from questions.models import Profile, Tag, Question, Answer, LikeDislike


class Command(BaseCommand):
    @staticmethod
    def generate_profiles():
        user_names = ['AliceSitedge', 'AntonyMo', 'LenkaDEA', 'aria_ramm', 'lavender_from_the_valley']
        for name in user_names:
            Profile.objects.create(user=User.objects.create_user(username=name, password='myawesamepass'),
                                   nickname=name,
                                   avatar='/avatar/' + name + '.png')

    @staticmethod
    def generate_tags():
        tags = ['django', 'python', 'web', 'geography', 'traveling', 'cinema', 'bestsellers', 'site', 'UX', 'fonts',
                'git', 'algorithms']
        for tag in tags:
            Tag.objects.create(name=tag)

    @staticmethod
    def generate_questions_answers():
        question_titles = ['How to do Web homework?',
                           'What is the capital of Chezh Republic?',
                           'Why everybody likes Joker?',
                           'What is decorator?',
                           'How to add a question on this site?',
                           'How to run a command?',
                           'How to choose fonts for a site?',
                           'How to create a django project?',
                           'How to move model managers to another file?',
                           'How to reset a commit without deleting files?',
                           'How to do sorting in multiple threads?']
        question_texts = ['Really, how?',
                          'I have a homework at school and my teacher doesn\'t know',
                          'I can\'t decide whether to go to the cinema or not',
                          'Explain please',
                          'The only way I found is to enter path \'ask-alice/ask\' but there should have been '
                          'another way...',
                          'I\'ve written a command in generate_data.py but cannot execute it, help please',
                          'Can\'t choose beautiful fonts for my site, everything looks awful',
                          'Never tried this before',
                          'I\'m trying to do this but end up with ModuleNotFoundError',
                          'I\'m scared',
                          'And what sorting is better']
        question_tags = [['django', 'python', 'web'],
                         ['geography', 'traveling'],
                         ['cinema', 'bestsellers'],
                         ['python'],
                         ['site', 'UX'],
                         ['django', 'python'],
                         ['web', 'site', 'fonts'],
                         ['django', 'web'],
                         ['django', 'python'],
                         ['git'],
                         ['algorithms']]
        question_answers = [['Read tutorials', 'Ask friends'],
                            ['Prague'],
                            ['It\'s a fantastic film', 'The actor\'s play is good',
                             'You should see it', 'Everywhere I go'],
                            ['Syntactic sugar'],
                            ['It\'s two days that I\'ve been trying to find it but it seems quite useless',
                             'Sorry, guys, the button will be added soon, I\'m currently adding some questions '
                             'and answers to database'],
                            ['Try \'python manage.py generate_data\''],
                            ['Try to search on fonts.google.com, they offer popular pairings as well, it\'s '
                             'very useful', 'Montserrat is my favourite', 'I like Quicksand'],
                            ['Never wanted more', 'https://docs.djangoproject.com/en/2.2/intro/tutorial01/'],
                            ['Do not import in managers, use self.object (for example)'],
                            ['Use --soft but do a pair of backups just in case', '--soft is a default parameter'],
                            ['For example https://neerc.ifmo.ru/wiki/index.php']]

        for i in range(len(question_titles)):
            q = Question(author=Profile.objects.get(id=randint(1, Profile.objects.count())),
                         title=question_titles[i],
                         text=question_texts[i])
            q.save()
            for tag_name in question_tags[i]:
                q.tags.add(Tag.objects.get(name=tag_name))
            q.save()
            for text in question_answers[i]:
                ans = Answer(author=Profile.objects.get(id=randint(1, Profile.objects.count())),
                             question=q,
                             text=text)
                ans.save()

    @staticmethod
    def generate_votes(object_type, num):
        for _ in range(num):
            vote = LikeDislike(vote=choice((1, -1)),
                               author=Profile.objects.get(id=randint(1, Profile.objects.count())),
                               content_object=object_type.object.get(id=randint(1, object_type.object.count())))
            vote.content_object.rating += vote.vote
            vote.content_object.save()
            vote.save()

    def handle(self, *args, **options):
        self.generate_profiles()
        self.generate_tags()
        self.generate_questions_answers()
        self.generate_votes(Question, 100)
        self.generate_votes(Answer, 100)
