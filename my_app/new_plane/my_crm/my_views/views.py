from django.shortcuts import render, redirect, HttpResponse, reverse
from my_crm import models
from my_crm.forms import RegForm, CustomerForm
import hashlib
from django.conf import global_settings
from django.contrib.sessions.backends import db
from django.views import View
from django.db.models import Q
from my_crm.utils.pagination import Pagination
from django.http.request import QueryDict


def index(request):
    return HttpResponse('index')


def login(request):
    err_msg = ''
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()
        obj = models.UserProfile.objects.filter(username=user, password=pwd, is_active=True).first()
        if obj:
            request.session['user_id'] = obj.pk
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
            form_obj.save()
            return redirect('/login/')

    return render(request, 'reg.html', {'form_obj': form_obj})


def customer_list(request):
    if request.path_info == reverse('customer_list'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True, )
    else:
        all_customer = models.Customer.objects.filter(consultant=request.account)

    return render(request, 'customer_list.html', {'all_customer': all_customer})


class CustomerList(View):

    def get(self, request):

        q = self.search(['qq', 'name', ])

        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True, )
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.account)

        pager = Pagination(request.GET.get('page', '1'), all_customer.count(), request.GET.copy(), 2)
        return render(request, 'customer_list.html', {
            'all_customer': all_customer[pager.start: pager.end],
            'page_html': pager.page_html
        })

    def post(self, request):
        action = request.POST.get('action')

        if not hasattr(self, action):
            return HttpResponse('非法操作')

        getattr(self, action)()

        return self.get(request)

    def multi_apply(self):
        ids = self.request.POST.getlist('id')
        models.Customer.objects.filter(id__in=ids).update(consultant=self.request.account)
    def multi_public(self):
        ids = self.request.POST.getlist('id')
        models.Customer.objects.filter(id__in=ids).update(consultant=None)
    def search(self, query_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q


userlist = [{'name': 'alex-{}'.format(i), 'pwd': "alexdsb-{}".format(i)} for i in range(1, 402)]


def user_list(request):
    try:
        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1
    except Exception as e:
        page = 1
    print(page)
    per_num = 15
    all_count = len(userlist)
    page_num, more = divmod(all_count, per_num)
    if more:
        page_num += 1
    max_show = 11
    half_show = max_show // 2

    if page_num < max_show:
        page_start = 1
        page_end = page_num
    else:
        if page <= half_show:
            page_start = 1
            page_end = max_show
        elif page + half_show > page_num:
            page_start = page_num - max_show + 1
            page_end = page_num
        else:
            page_start = page - half_show
            page_end = page + half_show

    """
    1  0   15
    2  15  30
    3  30  45
    """
    start = (page - 1) * per_num
    end = page * per_num

    li_list = []
    if page == 1:
        li_list.append('<li class="disabled" ><a> << </a></li>')
    else:
        li_list.append('<li ><a href="?page={}"> << </a></li>'.format(page - 1))

    for i in range(page_start, page_end + 1):
        if page == i:
            li_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
        else:
            li_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))

    if page == page_num:
        li_list.append('<li class="disabled" ><a> >> </a></li>')
    else:
        li_list.append('<li ><a href="?page={}"> >> </a></li>'.format(page + 1))

    page_html = ''.join(li_list)

    return render(request, 'user_list.html',
                  {"all_user": userlist[start:end],
                   'page_html': page_html
                   }, )


def user_list(request):
    pager = Pagination(request.GET.get('page', '1'), len(userlist), per_num=10, max_show=15)

    return render(request, 'user_list.html',
                  {"all_user": userlist[pager.start:pager.end],
                   'page_html': pager.page_html
                   }, )
def customer_add(request):
    form_obj = CustomerForm()
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST)
        if form_obj.is_valid():

            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'customer_add.html', {'form_obj': form_obj})
def customer_edit(request, edit_id):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'customer_edit.html', {'form_obj': form_obj})
def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('customer_list'))
    return render(request, 'customer_change.html', {'form_obj': form_obj, 'edit_id': edit_id})
