from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from .managers import QuestionManager, AnswerManager, LikeDislikeManager


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatar/', default='/static/images/avatar.jpg')

    def __str__(self):
        return self.nickname


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=500, null=False)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    object = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=500)
    rating = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)

    object = AnswerManager()

    def __str__(self):
        return self.text


class LikeDislike(models.Model):
    VOTES = (
        (1, 'Like'),
        (-1, 'Dislike')
    )

    vote = models.IntegerField(choices=VOTES)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    object = LikeDislikeManager()

    def __str__(self):
        return str(self.vote) + ' ' + self.content_type.name + ' ' + str(self.object_id)
