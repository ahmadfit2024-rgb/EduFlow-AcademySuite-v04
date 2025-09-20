# =================================================================
# apps/learning/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: The QuizBuilderView now has a fully
# functional post method. This is a critical update that allows
# instructors to create and save interactive quizzes, a core
# feature of the instructor's toolkit.
# =================================================================

from django.views.generic import DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from bson import ObjectId

from .models import Course, LearningPath, Lesson, Question, Answer
from .forms import LearningPathForm, LessonForm
from apps.enrollment.models import Enrollment

# ... (LessonDetailView, LearningPathCreateView, PathBuilderView, CourseManageView, LessonCreateView remain unchanged from previous update) ...
class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'learning/lesson_detail.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        lesson_order = self.kwargs.get('lesson_order')
        sorted_lessons = sorted(course.lessons, key=lambda l: l.order)
        current_lesson = next((l for l in sorted_lessons if l.order == lesson_order), None)
        if not current_lesson:
            if sorted_lessons:
                return redirect('learning:lesson_detail', course_slug=course.slug, lesson_order=sorted_lessons[0].order)
            return redirect('dashboard')
        current_lesson_index = sorted_lessons.index(current_lesson)
        prev_lesson_order = sorted_lessons[current_lesson_index - 1].order if current_lesson_index > 0 else None
        next_lesson_order = sorted_lessons[current_lesson_index + 1].order if current_lesson_index < len(sorted_lessons) - 1 else None
        try:
            enrollment = Enrollment.objects.get(student=self.request.user, enrollable_id=str(course._id))
            progress = enrollment.progress
            enrollment.last_accessed_lesson_id = str(current_lesson._id)
            enrollment.save()
        except Enrollment.DoesNotExist:
            progress = 0
        context.update({
            'sorted_lessons': sorted_lessons,
            'current_lesson': current_lesson,
            'prev_lesson_order': prev_lesson_order,
            'next_lesson_order': next_lesson_order,
            'progress': progress,
        })
        return context

class LearningPathCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = LearningPath
    form_class = LearningPathForm
    template_name = 'learning/path_form.html'
    def test_func(self):
        return self.request.user.role in ['admin', 'supervisor']
    def get_success_url(self):
        return reverse('learning:path_builder', kwargs={'pk': self.object.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create New Learning Path"
        return context

class PathBuilderView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = LearningPath
    template_name = 'learning/path_builder.html'
    context_object_name = 'learning_path'
    def test_func(self):
        return self.request.user.role in ['admin', 'supervisor']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        learning_path = self.get_object()
        path_course_ids = [module['course_id'] for module in learning_path.modules]
        context['available_courses'] = Course.objects.exclude(_id__in=path_course_ids)
        return context

class CourseManageView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Course
    template_name = 'learning/manage_course.html'
    context_object_name = 'course'
    def test_func(self):
        return self.request.user.role == 'admin' or self.get_object().instructor == self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_form'] = LessonForm()
        return context

class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        lesson = form.save(commit=False)
        max_order = max([l.order for l in course.lessons], default=0)
        lesson.order = max_order + 1
        lesson._id = ObjectId()
        video_url = form.cleaned_data.get('video_url')
        if lesson.content_type == 'video' and video_url:
            lesson.content_data = {'video_url': video_url}
        course.lessons.append(lesson)
        course.save()
        return render(self.request, 'partials/_lesson_list.html', {'course': course})

class QuizBuilderView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Handles both displaying the quiz builder interface and processing
    the submitted quiz data.
    """
    model = Course
    template_name = 'learning/quiz_builder.html'
    pk_url_kwarg = 'course_pk'
    context_object_name = 'course'

    def test_func(self):
        # Only admins or the course instructor can build quizzes
        return self.request.user.role == 'admin' or self.get_object().instructor == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_id = self.kwargs['lesson_id']
        lesson = next((l for l in self.object.lessons if str(l._id) == lesson_id), None)
        context['lesson'] = lesson
        return context

    def post(self, request, *args, **kwargs):
        course = self.get_object()
        lesson_id = self.kwargs['lesson_id']
        lesson_index = next((i for i, l in enumerate(course.lessons) if str(l._id) == lesson_id), None)

        if lesson_index is None:
            messages.error(request, "Lesson not found.")
            return redirect('dashboard')

        quiz_data = {'questions': []}
        post_data = request.POST

        # Loop through questions based on the submitted form data
        i = 1
        while f'question-text-{i}' in post_data:
            question_text = post_data[f'question-text-{i}']
            correct_answer_identifier = post_data.get(f'is-correct-{i}') # e.g., '1-2'

            question_obj = {
                '_id': ObjectId(),
                'question_text': question_text,
                'answers': []
            }

            # Loop through answers for the current question
            j = 1
            while f'answer-text-{i}-{j}' in post_data:
                answer_text = post_data[f'answer-text-{i}-{j}']
                is_correct = correct_answer_identifier == f'{i}-{j}'
                
                answer_obj = {
                    '_id': ObjectId(),
                    'answer_text': answer_text,
                    'is_correct': is_correct
                }
                question_obj['answers'].append(answer_obj)
                j += 1
            
            quiz_data['questions'].append(question_obj)
            i += 1
        
        # Update the specific lesson's content_data in the course
        course.lessons[lesson_index].content_data = quiz_data
        course.save()

        messages.success(request, f"Quiz for '{course.lessons[lesson_index].title}' has been saved successfully.")
        return redirect('learning:course_manage', pk=course.pk)


class TakeQuizView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'learning/take_quiz.html'
    pk_url_kwarg = 'course_pk'
    context_object_name = 'course'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_id = self.kwargs['lesson_id']
        lesson = next((l for l in self.object.lessons if str(l._id) == lesson_id), None)
        if not lesson or lesson.content_type != 'quiz':
            return redirect('dashboard')
        context['lesson'] = lesson
        return context

class QuizResultView(LoginRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'learning/quiz_result.html'
    pk_url_kwarg = 'enrollment_pk'
    context_object_name = 'enrollment'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt_id = self.kwargs['attempt_id']
        attempt = next((att for att in self.object.quiz_attempts if att['attempt_id'] == attempt_id), None)
        if not attempt:
            return redirect('dashboard')
        context['attempt'] = attempt
        return context