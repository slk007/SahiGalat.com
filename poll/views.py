from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Choice, Vote, Topic, Comment
from .forms import AddCommentForm

def home(request):
    return render(request, 'home.html')


def question_list(request):
    questions = Question.objects.all().order_by('-updated')
    context = {'questions': questions}
    return render(request, 'poll/question_list.html', context)


def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)

        # getting percentage of votes
        total_votes = 0
        sahi, sahi_percentage = 0,0
        galat, galat_percentage = 0,0
        for choice in question.choice_set.all():
            if choice.choice_text.lower() == 'sahi':
                sahi = choice.votes
            elif choice.choice_text.lower() == 'galat':
                galat = choice.votes
            total_votes += choice.votes

        # if no voting has been done yet
        if total_votes != 0:
            sahi_percentage = (sahi/total_votes)*100
            galat_percentage = (galat/total_votes)*100

        # all comments
        comments = question.comments.all().order_by('-id')
        
        # making context 
        context = {'question': question,
            'total_votes': total_votes,
            'sahi_percentage': sahi_percentage, 
            'galat_percentage': galat_percentage,
            'comments': comments
            }
        
        return render(request, 'poll/question_detail.html', context)
    except Question.DoesNotExist:
        return render(request, 'poll/question_list.html', {'error': 'No such question found !!!'})

@login_required
def add_comment(request, pk):
    question = Question.objects.get(pk=pk)

    # adding comment
    if request.method == 'POST':
        form = AddCommentForm(request.POST or None)
        if form.is_valid():
            comment_text = request.POST.get('comment_text')
            comment = Comment.objects.create(question=question, user=request.user, comment_text=comment_text)
            comment.save()
            messages.success(request, 'Comment was added !!')
            return HttpResponseRedirect(reverse('question_detail', args=(question.id,)))
        else:
            messages.error(request, 'No comment was typed !!!')
            return HttpResponseRedirect(reverse('question_detail', args=(question.id,)))
    else:
        form = AddCommentForm()

    context = {'question': question, 'form': form}
    return render(request, 'poll/question_detail.html', context=context)


@login_required
def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/question_detail.html', {'question': question, 'error': 'You did not select a choice !!!'})
    else:
        if not question.user_can_vote(request.user):
            # can't vote
            messages.error(
                request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
            return HttpResponseRedirect(reverse('question_detail', args=(question.id,)))
        else:
            # can vote
            vote = Vote(user=request.user, question=question, choice=selected_choice)
            vote.save()
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('question_detail', args=(question.id,)))

def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            questions = Question.objects.filter(question_text__icontains=search)
            if not questions:
                try:
                    topic = Topic.objects.get(topic_name__exact=search)
                    questions = topic.questions.all()
                except Topic.DoesNotExist:
                    error_message = f"Nothing as '{ search }' found."
                    return render(request, 'poll/question_list.html', {'error': error_message})
            context = {'questions': questions}
            return render(request, 'poll/question_list.html', context)
        else:
            return redirect('question_list')
    return redirect('question_list')


def topic_list(request):
    topics = Topic.objects.all()
    context = { 'topics': topics }
    return render(request, 'poll/topic_list.html', context)


def topic_detail(request, pk):
    topic = Topic.objects.get(pk=pk)
    questions = topic.questions.all()
    context = { 'topic':topic, 'questions':questions }
    return render(request, 'poll/topic_detail.html', context)
