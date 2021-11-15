from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    # tag = models.Column(models.String(200))
    img = models.CharField(max_length=200)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    createdby_id = models.IntegerField()

    date_posted = models.DateTimeField(verbose_name='date posted', auto_now_add=True)
    time_posted = models.DateTimeField(verbose_name='time posted', auto_now=True)
