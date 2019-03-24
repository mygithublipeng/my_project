from django.shortcuts import render, redirect, HttpResponse, reverse
from crm import models
from crm.forms import RegForm
import hashlib
from rbac.service.permission import init_permisson

def login(request):
    err_msg = ''

    if request.method == 'POST':
        # 获取提交的数据
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # 对密码进行加密
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()
        # 查询
        obj = models.UserProfile.objects.filter(username=user, password=pwd, is_active=True).first()
        if obj:
            # 认证成功 保存用户的id在session中
            request.session['user_id'] = obj.pk
            # 权限信息的初始化
            init_permisson(request,obj)
            # 跳转到首页
            return redirect('/index/')
        err_msg = '用户名或密码错误'
    return render(request, 'login.html', {'err_msg': err_msg})


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


def reg(request):
    form_obj = RegForm()
    if request.method == 'POST':
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # 写入到数据库中
            # form_obj.cleaned_data.pop('re_password')
            # obj = models.UserProfile.objects.create(**form_obj.cleaned_data)
            # print(obj)
            form_obj.save()
            return redirect('/login/')

    return render(request, 'reg.html', {'form_obj': form_obj})
