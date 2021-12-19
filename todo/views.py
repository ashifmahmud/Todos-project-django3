from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
  return render(request,'todo/home.html')

def signupuser(request):

  if request.method == 'GET':
    return render(request, 'todo/signupuser.html',{'form':UserCreationForm()})

  else:
    #create a new user

    if request.POST['password1'] == request.POST['password2']:
      try:
        user=User.objects.create_user(request.POST['username'],password =request.POST['password1'])
        user.save()
        login(request,user)
        return redirect('currenttodos')

      except IntegrityError:
        return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),'error':'This user name has already been taken. Choose a new one'})

    else:
      
      return render(request, 'todo/signupuser.html',{'form':UserCreationForm(),'error':'Password did not match'})



def loginuser(request):

  if request.method == 'GET':
    return render(request, 'todo/loginuser.html',{'form':AuthenticationForm()})

  else:
    #create a new user
    user= authenticate(request, username=request.POST['username'],password=request.POST['password'])
    
    if user is None:
      return render(request, 'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username or Password did not match'})
    
    else:
      login(request,user)
      return redirect('currenttodos')



   
  


@login_required
def logoutuser(request):
  if request.method == 'POST':
    logout(request)
    return redirect('home')

@login_required
def createtodo(request):
  if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})


  else:

    try:
      form = TodoForm(request.POST)
      newtodo = form.save(commit=False)
      newtodo.user = request.user
      newtodo.save()
      return redirect('currenttodos')

    except ValueError:
      return render(request, 'todo/createtodo.html',{'form':TodoForm(),'error':'Bad data passed in. Try again.'})

@login_required
def currenttodos(request):
  todos = Todo.objects.filter(user=request.user, datecompleted__isnull =True)
  return render(request, 'todo/currenttodos.html',{'todos':todos})

@login_required
def completedtodos(request):
  todos = Todo.objects.filter(user=request.user, datecompleted__isnull =False).order_by('-datecompleted')
  return render(request, 'todo/completedtodos.html',{'todos':todos})

@login_required
def viewtodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)

  if request.method == 'GET':
    form = TodoForm(instance = todo)
    return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form})
  else:
    try:
     form = TodoForm(request.POST, instance=todo)
     form.save()
     return redirect('currenttodos')

    except ValueError:
      return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form, 'error':'Bad Info'})

@login_required
def completetodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
  if request.method == 'POST':
    todo.datecompleted = timezone.now()
    todo.save()
    return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
  if request.method == 'POST':
    
    todo.delete()
    return redirect('currenttodos')

