# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from .models import Blog, User
import cookies

_LOGIN_COOKIE_ = 'login'
_LOGIN_COOKIE_AGE_ = 604800  # 登录cookie七天失效

def index(request):
    blogs = None
    if _LOGIN_COOKIE_ in request.COOKIES:
        login_cookie = request.COOKIES[_LOGIN_COOKIE_]
        id, expire_time, md5 = cookies.parse_login_cookie(login_cookie)
        user = get_object_or_404(User, pk=id)
        if cookies.vefiry_login_cookie(id, user.password, expire_time, md5):
            blogs = Blog.objects.filter(user_id=id).order_by('-create_time')
        else:
            blogs = Blog.objects.all().order_by('-create_time')
    else:
        blogs = Blog.objects.all().order_by('-create_time')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/index.html', context)

def list(request):
    user = None
    blogs = None
    login_cookie = None
    if request.method == 'GET':
        if _LOGIN_COOKIE_ in request.COOKIES:
            login_cookie = request.COOKIES[_LOGIN_COOKIE_]
            id, expire_time, md5 = cookies.parse_login_cookie(login_cookie)
            user = get_object_or_404(User, pk=id)
            if cookies.vefiry_login_cookie(id, user.password, expire_time, md5):
                blogs = Blog.objects.filter(user_id=id).order_by('create_time')
            else:
                blogs = Blog.objects.all().order_by('-create_time')
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
        login_cookie = cookies.generate_login_cookie(user.id, user.password, _LOGIN_COOKIE_AGE_)
        blogs = Blog.objects.filter(user_id=user.id).order_by('-create_time')
    context = {
        'blogs': blogs,
    }
    response = render(request, 'blog/list.html', context)
    if login_cookie is not None:
        response.set_cookie(_LOGIN_COOKIE_, login_cookie)
    return response

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
