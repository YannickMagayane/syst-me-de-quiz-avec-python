from django.urls import path
from . import views


urlpatterns = [
    path('choose_course/', views.choose_course, name='choose_course'),
    path('start/<int:course_id>/', views.start_quiz, name='start_quiz'),
    path('question/<int:question_number>/', views.quiz_question, name='quiz_question'),
    path('complete/<int:completion_id>/', views.quiz_complete, name='quiz_complete'),
    path('report_cheating/<int:user_answer_id>/', views.report_cheating, name='report_cheating'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/user/<int:user_id>/', views.user_quiz_history, name='user_quiz_history'),
    path('admin_dashboard/report_cheating/<int:user_answer_id>/', views.report_cheating_admin, name='report_cheating_admin'),
    path('admin_dashboard/create_course/', views.create_course, name='create_course'),
    path('admin_dashboard/create_question/', views.create_question, name='create_question'),
    path('admin_dashboard/create_answer/', views.create_answer, name='create_answer'),
    path('admin_dashboard/course_percentages/', views.course_percentages, name='course_percentages'),

]
