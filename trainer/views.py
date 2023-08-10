from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Course, Question, Answer, UserAnswer, QuizCompletion
from .forms import CourseForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User
import random


@login_required
def choose_course(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'choose_course.html', {'courses': courses})


@login_required
def start_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    if QuizCompletion.objects.filter(user=request.user, course=course, is_finished=True).exists():
        return render(request, 'quiz_finished.html', {'course': course})

    questions = list(Question.objects.filter(course=course, is_active=True))
    random.shuffle(questions)
    request.session['questions'] = [q.id for q in questions]
    request.session['current_question'] = 1
    request.session['current_course'] = course_id
    return redirect('quiz_question', question_number=1)


@login_required
def quiz_question(request, question_number):
    if 'questions' not in request.session or int(question_number) > len(request.session['questions']):
        return render(request, 'no_questions_available.html')

    question_id = request.session['questions'][int(question_number) - 1]
    question = Question.objects.get(id=question_id)
    answers = question.answers.all()

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        selected_answer = Answer.objects.get(id=selected_answer_id)
        user_answer = UserAnswer.objects.create(
            user=request.user,
            question=question,
            selected_answer=selected_answer
        )
        request.session['current_question'] += 1

        if request.session['current_question'] <= len(request.session['questions']):
            return redirect('quiz_question', question_number=request.session['current_question'])
        else:
            completion = QuizCompletion.objects.create(
                user=request.user,
                course_id=request.session['current_course'],
                score=UserAnswer.objects.filter(user=request.user, is_cheating=False, is_blocked=False).count(),
                is_finished=True
            )
            return redirect('quiz_complete', completion_id=completion.id)

    return render(request, 'question.html', {'question': question, 'answers': answers})


@login_required
def quiz_complete(request, completion_id):
    completion = get_object_or_404(QuizCompletion, id=completion_id)
    if completion.user != request.user or completion.is_blocked:
        return render(request, 'quiz_finished.html', {'course': completion.course})
    return render(request, 'quiz_complete.html', {'completion': completion})


@login_required
def report_cheating(request, user_answer_id):
    user_answer = get_object_or_404(UserAnswer, id=user_answer_id)
    user_answer.is_cheating = True
    user_answer.is_blocked = True
    user_answer.save()
    return redirect('quiz_question', question_number=request.session['current_question'])


@staff_member_required
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})


@staff_member_required
def user_quiz_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    completions = QuizCompletion.objects.filter(user=user)
    return render(request, 'user_quiz_history.html', {'user': user, 'completions': completions})


@staff_member_required
def report_cheating_admin(request, user_answer_id):
    user_answer = get_object_or_404(UserAnswer, id=user_answer_id)
    user_answer.is_cheating = True
    user_answer.is_blocked = True
    user_answer.save()
    return redirect('user_quiz_history', user_id=user_answer.user.id)

@login_required
@staff_member_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@login_required
@staff_member_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'create_question.html', {'form': form})

@login_required
@staff_member_required
def create_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AnswerForm()
    return render(request, 'create_answer.html', {'form': form})


from django.contrib.auth.models import User
from .models import Course, UserAnswer


@staff_member_required
def course_percentages(request):
    courses = Course.objects.all()
    users = User.objects.filter(is_staff=False)
    percentages = []

    for course in courses:
        course_percentages = []

        for user in users:
            user_answers = UserAnswer.objects.filter(user=user, question__course=course, is_cheating=False,
                                                     is_blocked=False)
            total_user_answers = user_answers.count()
            total_correct_answers = user_answers.filter(selected_answer__is_correct=True).count()
            total_correct_questions = Answer.objects.filter(question__course=course, is_correct=True).count()

            if total_correct_questions > 0:
                percentage = (total_correct_answers / total_correct_questions) * 100
            else:
                percentage = 0

            course_percentages.append((user, percentage))

        percentages.append((course, course_percentages))

    return render(request, 'course_percentages.html', {'percentages': percentages, 'users': users})
