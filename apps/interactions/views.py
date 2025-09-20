# =================================================================
# apps/interactions/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file is updated with a new view,
# AddDiscussionPostView, which handles the logic for posting replies.
# This makes the discussion forum a fully interactive, two-way
# communication tool as intended.
# =================================================================

from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render

from .models import DiscussionThread, DiscussionPost
from .forms import DiscussionThreadForm, DiscussionPostForm
from apps.learning.models import Course

class AddDiscussionThreadView(LoginRequiredMixin, CreateView):
    model = DiscussionThread
    form_class = DiscussionThreadForm
    
    def form_valid(self, form):
        course_id = self.request.POST.get('course_id')
        lesson_id = self.kwargs.get('lesson_id')
        course = get_object_or_404(Course, pk=course_id)
        
        thread = form.save(commit=False)
        thread.student = self.request.user
        thread.course_id = course_id
        thread.lesson_id = lesson_id
        thread.save()

        # After saving, re-render the list of discussions to show the new one
        threads = DiscussionThread.objects.filter(lesson_id=lesson_id).order_by('-created_at')
        context = {
            'threads': threads,
            'course': course,
            'current_lesson_id': lesson_id
        }
        
        response = render(self.request, 'interactions/partials/_discussion_list.html', context)
        # Use HTMX to trigger a global toast notification on success
        response['HX-Trigger-Detail'] = '{"message": "Your question has been posted successfully!"}'
        response['HX-Trigger'] = 'showToast'
        return response

class AddDiscussionPostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Handles adding a reply (post) to a discussion thread via HTMX.
    """
    model = DiscussionPost
    form_class = DiscussionPostForm
    template_name = 'interactions/partials/_thread_detail.html'

    def test_func(self):
        # Allow any authenticated user to reply for now.
        # Can be restricted to just instructors and the original student later.
        return self.request.user.is_authenticated

    def form_valid(self, form):
        thread = get_object_or_404(DiscussionThread, pk=self.kwargs['thread_id'])
        
        post = form.save(commit=False)
        post.thread = thread
        post.user = self.request.user
        post.save()
        
        # After saving, re-render the thread detail partial to update the UI
        # This will replace the thread content with the newly added reply.
        context = {'thread': thread}
        response = render(self.request, self.template_name, context)
        response['HX-Trigger-Detail'] = '{"message": "Your reply has been posted."}'
        response['HX-Trigger'] = 'showToast'
        return response

class AIChatFormView(LoginRequiredMixin, TemplateView):
    template_name = 'interactions/partials/_ai_chat_form.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'course_pk': self.kwargs.get('course_pk'),
            'lesson_id': self.kwargs.get('lesson_id'),
        })
        return context