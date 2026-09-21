from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TaskForm
from .models import Task

@login_required
def dashboard(request):
    tasks=Task.objects.filter(owner=request.user)
    query=request.GET.get("q","").strip()
    status=request.GET.get("status","")
    priority=request.GET.get("priority","")
    if query: tasks=tasks.filter(Q(title__icontains=query)|Q(description__icontains=query))
    if status=="completed": tasks=tasks.filter(completed=True)
    elif status=="pending": tasks=tasks.filter(completed=False)
    if priority in {"LOW","MEDIUM","HIGH"}: tasks=tasks.filter(priority=priority)
    all_tasks=Task.objects.filter(owner=request.user)
    return render(request,"tasks/dashboard.html",{
        "tasks":tasks,"query":query,"status":status,"priority":priority,
        "total_count":all_tasks.count(),
        "completed_count":all_tasks.filter(completed=True).count(),
        "pending_count":all_tasks.filter(completed=False).count(),
        "high_priority_count":all_tasks.filter(priority=Task.Priority.HIGH,completed=False).count(),
    })

@login_required
def create_task(request):
    form=TaskForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        task=form.save(commit=False); task.owner=request.user; task.save()
        messages.success(request,"Task created successfully.")
        return redirect("dashboard")
    return render(request,"tasks/task_form.html",{"form":form,"page_title":"Create Task"})

@login_required
def update_task(request,pk):
    task=get_object_or_404(Task,pk=pk,owner=request.user)
    form=TaskForm(request.POST or None,instance=task)
    if request.method=="POST" and form.is_valid():
        form.save(); messages.success(request,"Task updated successfully."); return redirect("dashboard")
    return render(request,"tasks/task_form.html",{"form":form,"page_title":"Update Task"})

@login_required
def delete_task(request,pk):
    task=get_object_or_404(Task,pk=pk,owner=request.user)
    if request.method=="POST":
        task.delete(); messages.success(request,"Task deleted successfully."); return redirect("dashboard")
    return render(request,"tasks/task_confirm_delete.html",{"task":task})

@login_required
def toggle_task(request,pk):
    task=get_object_or_404(Task,pk=pk,owner=request.user)
    if request.method=="POST":
        task.completed=not task.completed; task.save(update_fields=["completed","updated_at"])
    return redirect("dashboard")

def register(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form=UserCreationForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,"Account created successfully."); return redirect("dashboard")
    return render(request,"registration/register.html",{"form":form})

def health_check(request):
    return JsonResponse({"status":"healthy","service":"django-task-manager"})
