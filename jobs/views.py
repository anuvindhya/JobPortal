from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Job
from .models import Application
from .forms import Jobform
# 1. Job List
class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'all_jobs'
# 2. Job Detail
class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['already_applied'] = Application.objects.filter(
                job=self.object,
                applicant=self.request.user
            ).exists()
        return context
# 3. Create Job - Employer only
class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = Jobform
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job-list')
    def test_func(self):
        return self.request.user.role == 'employer'
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(
            self.request,
            'Job posted successfully!'
        )
        return super().form_valid(form)
# 4. Update Job - Owner only

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Job
    form_class = Jobform
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job-list')

    def test_func(self):

        job = self.get_object()

        return (
            self.request.user.role == 'employer'
            and job.posted_by == self.request.user
        )


# 5. Delete Job - Owner only

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job-list')

    def test_func(self):

        job = self.get_object()

        return (
            self.request.user.role == 'employer'
            and job.posted_by == self.request.user
        )


# 6. Apply for Job - Job Seeker only

@login_required
def apply_to_job(request, pk):

    job = get_object_or_404(Job, pk=pk)

    if request.user.role != 'job_seeker':

        messages.error(
            request,
            'Only Job Seekers can apply for jobs.'
        )

        return redirect('job-detail', pk=pk)

    if request.method == 'POST':

        application, created = Application.objects.get_or_create(
            job=job,
            applicant=request.user
        )

        if created:

            messages.success(
                request,
                'Your application was submitted successfully!'
            )

        else:

            messages.warning(
                request,
                'You have already applied for this job.'
            )

        return redirect('application-success')

    return redirect('job-detail', pk=pk)


# 7. My Jobs - Employer

class MyJobsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Job
    template_name = 'jobs/my_jobs.html'
    context_object_name = 'all_jobs'

    def test_func(self):

        return self.request.user.role == 'employer'

    def get_queryset(self):

        return Job.objects.filter(
            posted_by=self.request.user
        )


# 8. My Applications - Job Seeker

class MyApplicationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Application
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'

    def test_func(self):

        return self.request.user.role == 'job_seeker'

    def get_queryset(self):

        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job')


# 9. Application Success

@login_required
def application_success(request):
    return render(
        request,
        'jobs/application_success.html'
    )
@login_required
def dashboard(request):
    return render(request, 'jobs/dashboard.html')