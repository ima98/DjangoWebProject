"""
Definition of models.
"""

from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class User(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)


#copias de los modelos
class Question2(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    subject= models.CharField(max_length=200, default="")
    numChoices =models.IntegerField(default=4)

class Choice2(models.Model):
    question = models.ForeignKey(Question2)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    isCorrect = models.BooleanField(default=False)

class User2(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)