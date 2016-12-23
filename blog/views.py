# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from .models import Blog, User

def index(request):
    blogs = Blog.objects.all()
    context = {
               'blogs': blogs,
               }
    return render(request, 'blog/index.html', context)

def list(request):
    blogs = Blog.objects.filter(user_id=1)
    context = {
               'blogs': blogs,
               }
    return render(request, 'blog/list.html', context)

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    context = {
               'blog': blog,
               }
    return render(request, 'blog/detail.html', context)

def register(request):
    return render(request, 'blog/register.html')

def login(request):
    return render(request, 'blog/login.html')

def write(request):
    return render(request, 'blog/write.html')
