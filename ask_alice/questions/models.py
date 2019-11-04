from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    avatar = models.ImageField()

    def __str__(self):
        return self.nickname


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=500)
    rating = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    )

    vote = models.IntegerField(choices=VOTES)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
