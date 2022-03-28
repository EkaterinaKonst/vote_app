import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField('Вопрос',max_length=200)
    pub_date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug':self.slug})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('Текст ответа',max_length=200)
    votes = models.IntegerField('Голоса, подсчет',default=0)

    def __str__(self):
        return self.choice_text
