from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
# from django.template import loader
# Create your views here.


# def index(request):
#     last_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ','.join([q.question_text for q in last_question_list])
#     # return HttpResponse(output)
#     # template = loader.get_template('../templates/polls/index.html')
#     context = {
#         'latest_question_list': last_question_list,
#     }
#     # return HttpResponse(template.render(context, request))
#     return render(request, '../templates/polls/index.html', context)


# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, '../templates/polls/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = '../templates/polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """返回最近发布的5个问卷."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = '../templates/polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = '../templates/polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, '../templates/polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
