from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from django.contrib import auth
from django.contrib.auth.models import User

def welcome(request):
    return render(request, 'welcome.html')

def work(request, todo_id=None):
    if todo_id is not None:  # todo_id가 전달된 경우
        todo_item = get_object_or_404(TodoItem, id=todo_id)
        return render(request, 'work.html', {'todo_item': todo_item})
    elif request.method == 'POST':  # POST 요청일 때
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        TodoItem.objects.create(title=title, description=description)
        return redirect('work_detail', todo_id=TodoItem.objects.latest('id').id)  # 생성된 항목의 ID로 리다이렉트
    else:  # GET 요청일 때
        return render(request, 'work.html')

def login(request):
    if request.method=='POST':
        email = request.POST['email']
        pwd = request.POST['pwd']

        user = auth.authenticate(request, username=email, password=pwd)

        if user is None:
            return redirect('/join')
        else:
            auth.login(request, user)
            return redirect('/')

    return render(request, 'login.html')
    
def join(request):

    if request.method=='POST':

        email = request.POST['email']
        if request.POST['pwd1']==request.POST['pwd2']:
            pwd = request.POST['pwd1']
            User.objects.create_user(username=email, password=pwd)
            user = auth.authenticate(request, username=email, password=pwd)

            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('/join')


    return render(request, 'join.html')

def logout(request):

    auth.logout(request)

    return redirect('/')

def update(request, todo_id):
    todo_item = get_object_or_404(TodoItem, id=todo_id)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        todo_item.title = title
        todo_item.description = description
        todo_item.save()
        return redirect('/')
    return render(request, 'update.html', {'todo_item': todo_item})

def delete(request, todo_id):
    todo_item = get_object_or_404(TodoItem, id=todo_id)
    if request.method == 'POST':
        todo_item.delete()
        return redirect('/')
    return render(request, 'delete.html', {'todo_item': todo_item}) 