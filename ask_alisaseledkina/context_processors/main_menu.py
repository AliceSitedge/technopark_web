from django.db.models import Count

from questions.models import Profile, Tag


def menu(request):
    try:
        profile = Profile.objects.get(id=request.user.id)
    except Profile.DoesNotExist:
        profile = None

    popular_tags = Tag.objects.annotate(questions_num=Count('question')).order_by('-questions_num')[0:5]
    best_members = Profile.objects.annotate(activity=Count('question') + Count('answer')).order_by('-activity')[0:5]

    return {
        'user': request.user,
        'profile': profile,
        'popular_tags': popular_tags,
        'best_members': best_members
    }
