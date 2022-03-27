
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm, loginForm,postForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import blogPost
#Home
def home(request):
    posts = blogPost.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

#about
def about(request):
    return render(request,'blog/about.html')

#contact
def contact(request):
    return render(request,'blog/contact.html')

# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = blogPost.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'fname':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/blog/login/')

#SignUp
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! You have become author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = loginForm(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully !!')
                    return HttpResponseRedirect('/blog/dashboard/')
        else:
            form = loginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/dashboard/')

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = postForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['description']
                pst = blogPost(title=title, description = desc)
                pst.save()
                if pst is not None:
                    messages.success(request,'New Post Added Successfully!!')
                    form = postForm()
        else:
            form = postForm()
        return render(request, 'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/login/')

#update/edit post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blogPost.objects.get(pk=id)
            form = postForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                if form is not None:
                    messages.success(request,'Post is Updated Successfully!!')
        else:
            pi = blogPost.objects.get(pk=id)
            form = postForm(instance=pi)
        return render(request, 'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/login/')

#delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blogPost.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/blog/dashboard/')
    else:
        return HttpResponseRedirect('/blog/login/')
