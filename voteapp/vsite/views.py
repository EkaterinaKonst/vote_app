from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'vsite/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Возврат 5 последних опубликованных вопроса (не включая те, которые будут
        опубликованы в будущем)
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'vsite/detail.html'

    def get_queryset(self):
        """
    Исключает любые вопросы, которые еще не опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'vsite/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # повторное отображение формы голосования
        return render(request, 'vsite/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали ответ!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Всегда возвращает HttpResponseRedirect в случае успеха.
        # Это предотвращает повторную публикацию данных, если
        # пользователь нажимает кнопку "Назад"
        return HttpResponseRedirect(reverse('vsite:results', args=(question.id,)))