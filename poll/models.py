from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL #since we have customized the user model


class Topic(models.Model):
    topic_name = models.CharField(max_length=50)
    topic_description = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_name

class Question(models.Model):

    #foreign key
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 

    # adding related_name so that we can user .questions instead of .question_set
    topics = models.ManyToManyField(Topic, related_name="questions")
    
    question_text = models.CharField(max_length=200)
    question_description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=500)

    def user_can_vote(self,user):
        """Return False if user already voted"""
        user_votes = user.vote_set.all()
        qs = user_votes.filter(question=self)
        if qs.exists():
            return False
        return True

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.user.username}"" voted - "{self.choice.choice_text}"" for - "{self.question.question_text}"'
