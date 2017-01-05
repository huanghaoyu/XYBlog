# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import User
from .cookies import LOGIN_COOKIE
import cookies

class LoginAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if LOGIN_COOKIE in request.COOKIES:
            login_cookie = request.COOKIES[LOGIN_COOKIE]
            id, expire_time, md5 = cookies.parse_login_cookie(login_cookie)
            try:
                user = get_object_or_404(User, pk=id)
                if cookies.vefiry_login_cookie(id, user.password, expire_time, md5):
                    request.blog_user = user
            except Http404:
                pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    