import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвратит False для вопроса у которого поле pub_date
        в будущем числе
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() возвратит False для вопроса где pub_date
    старше дня.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() возвратит True для вопроса где pub_date
    в пределах дня.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Создает вопрос с заданным `question_text` и публикует заданное количество дней со смещением до настоящего времени
    (отрицательное значение для вопросов, опубликованных
    в прошлом, положительное значение для вопросов, которые еще не опубликованы).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Если вопросов нет, отображается соответствующее сообщение.
        """
        response = self.client.get(reverse('vsite:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Созданные правильно вопросы попадают в latest_question_list
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('vsite:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Создаётся опрос с pub_date в будущем. База данных сбрасывается для каждого тестового метода,
        так что список опросов пустой
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('vsite:index'))
        self.assertContains(response, "Нет доступных опросов")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Даже если существуют как прошлые, так и будущие вопросы, отображаются только прошлые вопросы
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('vsite:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        На странице с указателем вопросов может отображаться несколько вопросов.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('vsite:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
    detail view вопроса с pub_date в будущем возвращает 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('vsite:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        В detail view вопроса с pub_date в прошлом отображается текст вопроса.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('vsite:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)