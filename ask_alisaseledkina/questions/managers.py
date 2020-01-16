from django.db import models
from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404


class QuestionManager(models.Manager):
    def get_fresh(self):
        return self.annotate(answers_num=Count('answer')).order_by('-datetime')

    def get_hot(self):
        return self.annotate(answers_num=Count('answer')).order_by('-rating')

    def get_tag(self, tag_name):
        return get_list_or_404(self.annotate(answers_num=Count('answer')).filter(tags__name=tag_name))

    def get_question(self, question_id):
        return get_object_or_404(self.model, id=question_id)


class AnswerManager(models.Manager):
    def get_question(self, question_id):
        return self.model.object.filter(question__id=question_id).order_by('-datetime')


class LikeDislikeManager(models.Manager):
    def get_likes(self):
        return self.model.object.filter(vote='Like')

    def get_dislikes(self):
        return self.model.object.filter(vote='Dislike')

    def make_vote(self, profile, voted_object, object_type, vote_value):
        try:
            if object_type == 'question':
                vote = self.model.object.get(author=profile, question=voted_object)
            else:
                vote = self.model.object.get(author=profile, answer=voted_object)
        except self.model.DoesNotExist:
            vote = self.model.object.create(vote=vote_value,
                                            author=profile,
                                            content_object=voted_object)
            vote.content_object.rating += vote.vote
            vote.content_object.save()
            vote.save()
            return vote

        if vote.vote == vote_value:
            return vote

        vote.vote = vote_value
        vote.content_object.rating += 2 * vote.vote
        vote.content_object.save()
        vote.save()
        return vote
