from django.contrib import admin
from .models import Course, Question, Answer, UserAnswer, QuizCompletion

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'course', 'is_active']
    list_filter = ['course', 'is_active']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['question__course', 'is_correct']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'selected_answer', 'is_cheating', 'is_blocked']
    list_filter = ['user', 'question__course', 'is_cheating', 'is_blocked']

@admin.register(QuizCompletion)
class QuizCompletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completion_date', 'score', 'is_cheating', 'is_blocked', 'is_finished']
    list_filter = ['user', 'course', 'is_cheating', 'is_blocked', 'is_finished']
