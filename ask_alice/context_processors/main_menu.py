from django.db.models import Count

from questions.models import Profile, Tag

popular_tags = Tag.objects.annotate(questions_num=Count('question')).order_by('-questions_num')[0:5]
best_members = Profile.objects.annotate(activity=Count('question') + Count('answer')).order_by('-activity')[0:5]


def menu(request):
    return {
        'user': request.user,
        'popular_tags': popular_tags,
        'best_members': best_members
    }
