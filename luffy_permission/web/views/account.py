from django.shortcuts import HttpResponse, redirect, render, reverse
from rbac import models
from rbac.service.permission import init_permisson


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        obj = models.User.objects.filter(name=user, password=pwd).first()
        if not obj:
            return render(request, 'login.html', {'error_msg': '用户名或密码错误'})
        # 登陆成功  权限信息的初始化
        init_permisson(request, obj)

        return redirect(reverse('customer_list'))

    return render(request, 'login.html')


def index(request):
    return HttpResponse('这是index')
