# -*- coding: utf-8 -*-

import hashlib, time

LOGIN_COOKIE = 'login'
LOGIN_COOKIE_AGE = 604800  # 登录cookie七天失效

_COOKIE_SECRET_KEY_ = '&]}7,}hKpY8w>Fm@'

def generate_login_cookie(id, password, age):
    '''
    Calculate login cookie.
    
    id: user id.
    password: user password.
    age: cookie living time in seconds.
    
    cookie = id + expire_time + md5(id + password + expire_time + secretkey).
    '''
    expire_time = str(int(time.time() + age));
    return '-'.join([str(id), str(expire_time), hashlib.md5(str(id) + str(password) + str(expire_time) + str(_COOKIE_SECRET_KEY_)).hexdigest()])
    
def parse_login_cookie(login_cookie):
    return login_cookie.split('-')
    
def vefiry_login_cookie(id, password, expire_time, login_cookie):
    '''
    Vefiry login cookie.
    
    id: user id.
    password: user password.
    expire_time: expire time from client.
    login_cookie: login cookie from client.
    '''
    return login_cookie == hashlib.md5(str(id) + str(password) + str(expire_time) + str(_COOKIE_SECRET_KEY_)).hexdigest()
    