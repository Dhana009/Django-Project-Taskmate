from django.shortcuts import render, redirect
from todolist_app.models import tasklist
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def todolist(request):
    if request.method == "POST":
        form = Taskform(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage= request.user
            instance.save()
        messages.success(request, (' new task added '))
        return redirect('todolist')
    else:
        all_tasks = tasklist.objects.filter(manage=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {"all_tasks": all_tasks})
@login_required
def delete_task(request, task_id):
    task = tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()

    else:
        messages.error(request, ("you are not allowed"))

    return redirect('todolist')
@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = tasklist.objects.get(pk=task_id)
        form = Taskform(request.POST or None, instance= task)
        if form.is_valid():
            form.save()

        messages.success(request, ('Task edited! '))
    else:
        task_obj = tasklist.objects.get(pk=task_id)
        return render(request, 'edit.html', {"task_obj": task_obj})

    return redirect('todolist')
@login_required
def complete_task(request, task_id):
    task = tasklist.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("you are not allowed"))

    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()

    return redirect('todolist')
@login_required
def index(request):
    context = {
        'index_text': 'welcome to the index page'
    }
    return render(request, 'index.html', context)

def contact(request):
    context = {
        'contact_text': 'welcome to the contact page'
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'about_text': 'welcome to the about page'
    }
    return render(request, 'about.html', context)