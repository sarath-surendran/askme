from django.shortcuts import get_object_or_404, render, redirect
from .models import Question,Answer,Like
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.
def homeview(request):
    user = request.user
    try:
        questions = Question.objects.all().order_by('created_at')
    except Question.DoesNotExist:
        print('No questions')
    context = {
        'user': user,
        'questions': questions
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def create_question(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            question = form.save()
            return redirect('home')
        else:
            form = QuestionForm()

    return render(request, 'questions/add_question.html', {"form": form})


@login_required(login_url='login')
def show_question(request, question_id):
    form = AnswerForm()

    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(
        question=question).order_by('created_at')

    # like_status = False
    # try:
    #     Like.objects.filter(answer__in=answers, user=request.user)
    #     like_status = True
    # except Like.DoesNotExist:
    #     like_status = False

    liked_answers = []
    likes = Like.objects.filter(user=request.user)
    
    for like in likes:
        liked_answers.append(like.answer.id)
   

    context = {
        "form": form,
        "question": question,
        "user": question.user,
        'date': question.created_at,
        # "like_status": like_status,
        "answer": answers,
        "liked_answers":liked_answers
    }

    return render(request, 'questions/show_question.html', context)


@login_required(login_url='login')
def answer_question(request, question_id):
    form = AnswerForm()
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('show_question', question_id=question_id)
        else:
            form = form = AnswerForm()
    return render(request, 'questions/answer.html', {"form": form, "question": question})


@login_required(login_url='login')
def like(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        user = request.user
        liked, created = Like.objects.get_or_create(answer=answer, user=user)
        if created:
            messages.success(request, 'Liked successfully')
        elif liked:
            liked.delete()
            messages.success(request, 'Unliked succesfully')

        question_url = reverse('show_question', kwargs={
                               'question_id': answer.question.id})
        return redirect(question_url)
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponse(str(e))