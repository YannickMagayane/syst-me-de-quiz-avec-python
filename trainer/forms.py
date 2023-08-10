from django import forms
from .models import Course, Question, Answer

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'is_active']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'course', 'is_active']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'question', 'is_correct']
