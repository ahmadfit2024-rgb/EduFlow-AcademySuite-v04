from django.urls import path
from .views import (
    LessonDetailView, 
    PathBuilderView, 
    LearningPathCreateView,
    CourseManageView,
    LessonCreateView,
    QuizBuilderView,
    TakeQuizView,      # New import
    QuizResultView,    # New import
)

app_name = 'learning'

urlpatterns = [
    # ... (other URLs remain the same) ...
    path(
        'courses/<slug:course_slug>/lessons/<int:lesson_order>/', 
        LessonDetailView.as_view(), 
        name='lesson_detail'
    ),
    path(
        'paths/create/', 
        LearningPathCreateView.as_view(), 
        name='path_create'
    ),
    path(
        'paths/<str:pk>/build/', 
        PathBuilderView.as_view(), 
        name='path_builder'
    ),
    path(
        'courses/<str:pk>/manage/',
        CourseManageView.as_view(),
        name='course_manage'
    ),
    path(
        'courses/<str:course_pk>/add-lesson/',
        LessonCreateView.as_view(),
        name='lesson_add'
    ),
    path(
        'courses/<str:course_pk>/lessons/<str:lesson_id>/quiz-builder/',
        QuizBuilderView.as_view(),
        name='quiz_builder'
    ),

    # New URLs for taking a quiz and seeing results
    path(
        'courses/<str:course_pk>/lessons/<str:lesson_id>/take-quiz/',
        TakeQuizView.as_view(),
        name='take_quiz'
    ),
    path(
        'enrollment/<str:enrollment_pk>/quiz-result/<str:attempt_id>/',
        QuizResultView.as_view(),
        name='quiz_result'
    ),
]