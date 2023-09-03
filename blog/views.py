from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm,loginForm,PostForm
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
#Home
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def about(request):
    return render(request,'blog/about.html')
def contect(request):
    return render(request,'blog/contect.html')

def dashboard(request):
    if request.user.is_authenticated:
     posts=Post.objects.all()
     return render(request,'blog/dashboard.html',{'posts':posts})
    else:
       return HttpResponseRedirect('/login/')
    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method =='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
         messages.success(request,'Congratulation!! You have become an Author.')
         user=form.save()
         group = Group.objects.get(name='Author')
         user.groups.add(group)
    else:        
     form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})


def user_login(request):
   if not request.user.is_authenticated:
    if request.method =="POST":
      form=loginForm(request=request , data=request.POST)
      if form.is_valid():
        uname=form.cleaned_data['username']
        upass=form.cleaned_data['password']
        user=authenticate(username=uname,password=upass)
        if user is not None:
           login(request,user)
           messages.success(request,'Logged in Successfully !!')
           return HttpResponseRedirect('/dashboard/')
    else:
      form=loginForm()
      return render(request,'blog/login.html',{'form':form})
   else:
        return HttpResponseRedirect('/dashboard/')
    

def add_post(request):
   if request.user.is_authenticated:
      if request.method=='POST':
         form =PostForm(request.POST)
         if form.is_valid():
            title=form.cleaned_data['title']
            desc=form.cleaned_data['desc']
            pst=Post(title=title,desc=desc)
            pst.save()
            form=PostForm()
      else:
          form=PostForm()  
      return render(request,'blog/addpost.html',{'form':form})
   else:
      return HttpResponseRedirect('/login/')
   
def update_post(request):
   if request.user.is_authenticated:
     if request.method =='Post':
        pi=Post.objects.get(pk=id)
        form=PostForm(request.Post,instance=pi)
        if form.is_valid():
           form.save()
     else:
        pi=Post.objects.get(pk=id)
        form=PostForm(instance=pi)
     return render(request,'blog/updatepost.html',{'form':form})
   else:
      return HttpResponseRedirect('/login')      
   
def delete_post(request, id ):
   

   if request.user.is_authenticated:
      if request.method == 'POST':
         pi=Post.objects.get(pk=id)
         pi.delete()
         return HttpResponseRedirect('/dashboard/')
   else:
      return HttpResponseRedirect('/login/')