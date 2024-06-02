# voting_app/views.py
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, redirect

from .forms import ChoiceForm
from .models import Question, Choice


def index(request):
    questions = Question.objects.all()
    return render(request, 'myapp/index.html', {'questions': questions})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail', question_id=question_id)
    else:
        form = ChoiceForm(initial={'question': question})
    return render(request, 'myapp/detail.html', {'question': question, 'form': form})


# myapp/views.py
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Handle invalid choice
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "Please select a valid choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to results page
        return HttpResponseRedirect(reverse('detail', args=(question.id,)))
