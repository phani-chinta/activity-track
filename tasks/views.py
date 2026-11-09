from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Task


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing.html")


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    today = timezone.localdate()
    stats = tasks.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status=Task.Status.PENDING)),
        in_progress=Count("id", filter=Q(status=Task.Status.IN_PROGRESS)),
        completed=Count("id", filter=Q(status=Task.Status.COMPLETED)),
        overdue=Count("id", filter=Q(due_date__lt=today) & ~Q(status=Task.Status.COMPLETED)),
    )
    upcoming = tasks.exclude(status=Task.Status.COMPLETED).filter(due_date__gte=today).order_by("due_date", "created_at")[:5]
    return render(request, "tasks/dashboard.html", {"stats": stats, "upcoming": upcoming})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    query = request.GET.get("q", "").strip()
    priority = request.GET.get("priority", "")
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "due_date")
    if query:
        tasks = tasks.filter(title__icontains=query)
    if priority in Task.Priority.values:
        tasks = tasks.filter(priority=priority)
    if status in Task.Status.values:
        tasks = tasks.filter(status=status)
    tasks = tasks.order_by("-created_at" if sort == "newest" else "due_date", "-created_at")
    return render(request, "tasks/task_list.html", {"tasks": tasks, "query": query, "priority": priority, "status": status, "sort": sort, "priorities": Task.Priority.choices, "statuses": Task.Status.choices})


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Task created.")
        return redirect("task_detail", pk=task.pk)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Create a task"})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, "tasks/task_detail.html", {"task": task})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Task updated.")
        return redirect("task_detail", pk=task.pk)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Edit task", "task": task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.status = Task.Status.COMPLETED
        task.save(update_fields=["status", "updated_at"])
        messages.success(request, "Task marked complete.")
    return redirect("task_detail", pk=task.pk)
