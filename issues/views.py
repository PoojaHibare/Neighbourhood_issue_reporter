import json

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import IssueForm, LoginForm, RegisterForm
from .models import Issue

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
STATUS_STEPS = ['Reported', 'Verified', 'Assigned', 'In Progress', 'Resolved', 'Closed']

def home(request):
    return render(request, 'issues/home.html')

def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.status = 'Reported'
            issue.save()
            messages.success(request, 'Your issue has been submitted successfully. It is now visible on the Track and Dashboard pages.')
            return redirect('track_issues')
    else:
        form = IssueForm()
    return render(request, 'issues/report_issue.html', {'form': form})

def track_issues(request):
    issues = Issue.objects.all()
    counts = {
        'total': issues.count(),
        'pending': issues.filter(status='Reported').count(),
        'in_progress': issues.filter(status='In Progress').count(),
        'resolved': issues.filter(status='Resolved').count(),
    }
    return render(request, 'issues/track_issues.html', {'issues': issues, **counts})

def track_detail(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    progress = STATUS_STEPS
    current_index = progress.index(issue.status) if issue.status in progress else 0
    return render(request, 'issues/track_detail.html', {'issue': issue, 'progress': progress, 'active_index': current_index})

def dashboard(request):
    total = Issue.objects.count()
    pending = Issue.objects.filter(status='Reported').count()
    in_progress = Issue.objects.filter(status='In Progress').count()
    resolved = Issue.objects.filter(status='Resolved').count()
    recent_issues = Issue.objects.order_by('-created_at')[:5]
    status_counts = dict(Issue.objects.values_list('status').annotate(count=Count('id')))
    chart_labels = STATUS_STEPS
    chart_data = [status_counts.get(status, 0) for status in chart_labels]
    return render(request, 'issues/dashboard.html', {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'recent_issues': recent_issues,
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    })

def admin_login(request):
    error = None
    already_admin = request.session.get('is_admin', False)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            request.session['is_admin'] = True
            return redirect('admin_manage')
        error = 'Invalid credentials. Use admin / admin123.'
    return render(request, 'issues/admin_login.html', {'error': error, 'already_admin': already_admin})

def admin_logout(request):
    request.session.pop('is_admin', None)
    return redirect('admin_login')

def admin_manage(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        issue = get_object_or_404(Issue, pk=issue_id)
        action = request.POST.get('action')
        if action == 'verify':
            issue.status = 'Verified'
        elif action == 'reject':
            issue.status = 'Rejected'
        elif action == 'assign':
            department = request.POST.get('department', '')
            if department:
                issue.assigned_department = department
                issue.status = 'Assigned'
        elif action == 'update_status':
            status = request.POST.get('status')
            if status in [choice[0] for choice in Issue._meta.get_field('status').choices]:
                issue.status = status
        priority = request.POST.get('priority')
        if priority in [choice[0] for choice in Issue._meta.get_field('priority').choices]:
            issue.priority = priority
        issue.save()
        messages.success(request, f'Issue #{issue.id} updated successfully.')
        return redirect('admin_manage')
    issues = Issue.objects.all()
    return render(request, 'issues/admin_manage.html', {'issues': issues, 'status_choices': Issue._meta.get_field('status').choices, 'priority_choices': Issue._meta.get_field('priority').choices})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'issues/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(request, user)
        return redirect('home')
    return render(request, 'issues/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
