# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from .models import Blog, User
from .cookies import LOGIN_COOKIE, LOGIN_COOKIE_AGE
import cookies

def index(request):
    user = None
    blogs = None
    if hasattr(request, 'blog_user') and request.blog_user is not None:
        user = request.blog_user
        blogs = Blog.objects.filter(user_id=user.id).order_by('-create_time')
    else:
        blogs = Blog.objects.all().order_by('-create_time')
    context = {
        'user': user,
        'blogs': blogs,
    }
    return render(request, 'blog/index.html', context)

def list(request):
    user = None
    blogs = None
    login_cookie = None
    if request.method == 'GET':
        if LOGIN_COOKIE in request.COOKIES:
            login_cookie = request.COOKIES[LOGIN_COOKIE]
        if hasattr(request, 'blog_user') and request.blog_user is not None:
            user = request.blog_user
            blogs = Blog.objects.filter(user_id=user.id).order_by('-create_time')
        else:
            blogs = Blog.objects.all().order_by('-create_time')
    elif request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if name == '':
            # 登录
            try:
                user = get_object_or_404(User, email=email)
            except Http404:
                messages.add_message(request, messages.WARNING, u'账户不存在！')
                return redirect(reverse('blog:login'))
            if password != user.password:
                messages.add_message(request, messages.WARNING, u'密码错误！')
                return redirect(reverse('blog:login'))
        else:
            # 注册
            try:
                user = get_object_or_404(User, email=email)
                messages.add_message(request, messages.WARNING, u'电子邮箱已被注册！')
                return redirect(reverse('blog:register'))
            except Http404:
                user = User(name=name, email=email, password=password)
                user.save()
        login_cookie = cookies.generate_login_cookie(user.id, user.password, LOGIN_COOKIE_AGE)
        blogs = Blog.objects.filter(user_id=user.id).order_by('-create_time')
    context = {
        'user': user,
        'blogs': blogs,
    }
    response = render(request, 'blog/list.html', context)
    if login_cookie is not None:
        response.set_cookie(LOGIN_COOKIE, login_cookie)
    return response

def detail(request, blog_id):
    user = None
    blog = None
    if hasattr(request, 'blog_user') and request.blog_user is not None:
        user = request.blog_user
    if int(blog_id) == 0:
        if request.method == 'POST':
            # 新建博客
            title = request.POST.get('title', 'No title')
            summary = request.POST.get('summary', 'No summary')
            content = request.POST.get('content', 'No content')
            if 'image' in request.FILES:
                blog = Blog(title=title, summary=summary, content=content, user=user, image=request.FILES['image'])
            else:
                blog = Blog(title=title, summary=summary, content=content, user=user)
            blog.save()
    else:
        # 显示已有博客
        blog = get_object_or_404(Blog, pk=blog_id)
        print type(blog.image)
        print blog.image
    context = {
        'user': user,
        'blog': blog,
    }
    return render(request, 'blog/detail.html', context)

def register(request):
    return render(request, 'blog/register.html')

def login(request):
    return render(request, 'blog/login.html')

def write(request):
    user = None
    if hasattr(request, 'blog_user') and request.blog_user is not None:
        user = request.blog_user
    context = {
        'user': user,
    }
    return render(request, 'blog/write.html', context)
