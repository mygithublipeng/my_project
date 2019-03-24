from django.shortcuts import render, redirect, HttpResponse, reverse
from crm import models
from crm.forms import RegForm, CustomerForm, ConsultForm, EnrollmentForm
import hashlib
from django.conf import global_settings
from django.contrib.sessions.backends import db
from django.views import View
from django.db.models import Q
from crm.utils.pagination import Pagination
from crm.utils.url import reverse_url, rev_url
from django.db import transaction
from django.conf import settings


def index(request):
    return HttpResponse('index')




# 客户展示
def customer_list(request):
    if request.path_info == reverse('customer_list'):
        all_customer = models.Customer.objects.filter(consultant__isnull=True, )
    else:
        # 私户
        all_customer = models.Customer.objects.filter(consultant=request.account)

    return render(request, 'consultant/customer_list.html', {'all_customer': all_customer})


class CustomerList(View):

    def get(self, request):

        q = self.search(['qq', 'name', ])

        if request.path_info == reverse('customer_list'):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True, )
        else:
            # 私户
            all_customer = models.Customer.objects.filter(q, consultant=request.account)

        pager = Pagination(request.GET.get('page', '1'), all_customer.count(), request.GET.copy(), 10)
        return render(request, 'consultant/customer_list.html', {
            'all_customer': all_customer[pager.start: pager.end],
            'page_html': pager.page_html
        })

    def post(self, request):
        action = request.POST.get('action')

        if not hasattr(self, action):
            return HttpResponse('非法操作')

        res = getattr(self, action)()
        # 如果操作中有返回值，直接返回res
        if res:
            return res

        return self.get(request)

    def multi_apply(self):
        # 公户变私户
        ids = self.request.POST.getlist('id')
        # 方式一
        # models.Customer.objects.filter(id__in=ids).update(consultant=self.request.account)

        # 如果当前有的私户+申请的数量 》 最大值  不允许
        if self.request.account.customers.all().count() + len(ids) > settings.MAX_CUSTOMER_NUM:
            return HttpResponse('做人不能太贪心了')

        # 事务
        with transaction.atomic():
            # 查询出数据加锁
            queryset = models.Customer.objects.filter(id__in=ids, consultant__isnull=True).select_for_update()  # 加锁

            if len(ids) == queryset.count():
                queryset.update(consultant=self.request.account)
                return
            return HttpResponse('你的手速太慢了，已经被别人抢走了')

        # 方式二
        # self.request.account.customers.add(*models.Customer.objects.filter(id__in=ids))

    def multi_public(self):
        ids = self.request.POST.getlist('id')
        # 方式一
        models.Customer.objects.filter(id__in=ids).update(consultant=None)
        # 方式二
        # self.request.account.customers.remove(*models.Customer.objects.filter(id__in=ids))

    def search(self, query_list):
        query = self.request.GET.get('query', '')

        # Q(Q(qq__contains=query) | Q(name__contains=query))
        q = Q()
        q.connector = 'OR'

        #  Q(('qq__contains', query))    Q(qq__contains=query)
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q


userlist = [{'name': 'alex-{}'.format(i), 'pwd': "alexdsb-{}".format(i)} for i in range(1, 402)]


def user_list(request):
    # 当前的页码数
    try:
        page = int(request.GET.get('page', '1'))
        if page <= 0:
            page = 1
    except Exception as e:
        page = 1
    print(page)
    # 每页显示的数据条数
    per_num = 15
    # 总数据量
    all_count = len(userlist)
    # 总页码数
    page_num, more = divmod(all_count, per_num)
    if more:
        page_num += 1
    # 最多显示页码数
    max_show = 11
    half_show = max_show // 2

    if page_num < max_show:
        # 总页码数不够 最大显示页码数
        page_start = 1
        page_end = page_num
    else:
        # 能显示超过最大显示页码数
        if page <= half_show:
            # 处理左边的极值
            page_start = 1
            page_end = max_show
        elif page + half_show > page_num:
            # 处理右边的极值
            page_start = page_num - max_show + 1
            page_end = page_num
        else:
            # 正常的情况
            page_start = page - half_show
            page_end = page + half_show

    """
    1  0   15
    2  15  30
    3  30  45
    """
    # 切片的起始值
    start = (page - 1) * per_num
    # 切片的终止值
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
                   # 'page_num': range(page_start, page_end + 1),
                   'page_html': page_html
                   }, )


def user_list(request):
    pager = Pagination(request.GET.get('page', '1'), len(userlist), per_num=10, max_show=15)

    return render(request, 'user_list.html',
                  {"all_user": userlist[pager.start:pager.end],
                   'page_html': pager.page_html
                   }, )


# 增加客户
def customer_add(request):
    # 创建一个空的form对象
    form_obj = CustomerForm()
    if request.method == 'POST':
        # 创建一个包含提交数据的form对象
        form_obj = CustomerForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            # 保存数据
            form_obj.save()  # 新增
            # 跳转至展示页面
            return redirect(reverse('customer_list'))
    return render(request, 'consultant/customer_add.html', {'form_obj': form_obj})


# 编辑客户
def customer_edit(request, edit_id):
    # 查询出要编辑的对象
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        # 把元数据和新的数据较给form
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 对要修改的对象进行修改
            # 跳转至展示页面
            return redirect(reverse('customer_list'))
    return render(request, 'consultant/customer_edit.html', {'form_obj': form_obj})


# 新增和编辑
def customer_change(request, edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    form_obj = CustomerForm(instance=obj)
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()  # 没有instance新增  有instance做修改
            # return redirect(reverse('customer_list'))
            # return redirect(reverse_url(request, 'customer_list'))
            return redirect(rev_url(request, 'customer_list'))
    return render(request, 'consultant/customer_change.html', {'form_obj': form_obj, 'edit_id': edit_id})


class ConsultList(View):
    def get(self, request, customer_id):
        # 获取跟进记录
        if customer_id == '0':
            all_consult = models.ConsultRecord.objects.filter(consultant=request.account)
        else:
            all_consult = models.ConsultRecord.objects.filter(consultant=request.account, customer_id=customer_id)
        return render(request, 'consultant/consult_list.html', {'all_consult': all_consult})


def consult_add(request):
    # 实例化一个包含当前销售的跟进记录
    obj = models.ConsultRecord(consultant=request.account)
    form_obj = ConsultForm(instance=obj)
    # 处理POST请求
    if request.method == 'POST':
        # 实例化一个带提交参数的form
        form_obj = ConsultForm(request.POST, instance=obj)
        # 校验数据
        if form_obj.is_valid():
            form_obj.save()  # 新增
            return redirect(reverse('consult_list', args=('0')))

    return render(request, 'consultant/consult_add.html', {'form_obj': form_obj})


def consult_edit(request, edit_id):
    # 查询出要编辑的对象
    obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
    form_obj = ConsultForm(instance=obj)
    # 处理POST请求
    if request.method == 'POST':
        # 实例化一个带提交参数的form
        form_obj = ConsultForm(request.POST, instance=obj)
        # 校验数据
        if form_obj.is_valid():
            form_obj.save()  # 新增
            return redirect(reverse('consult_list', args=('0')))
    return render(request, 'consultant/consult_edit.html', {'form_obj': form_obj})


class EnrollmentList(View):
    def get(self, request, customer_id):
        # 获取跟进记录
        if customer_id == '0':
            all_enrollment = models.Enrollment.objects.filter(customer__in=request.account.customers.all())
        else:
            all_enrollment = models.Enrollment.objects.filter(customer_id=customer_id)
        return render(request, 'consultant/enrollment_list.html', {'all_enrollment': all_enrollment})


def enrollment_add(request, customer_id):
    obj = models.Enrollment(customer_id=customer_id)
    form_obj = EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment_list', args=('0')))
    return render(request, 'form.html', {'form_obj': form_obj, 'title': '添加报名记录'})


def enrollment_edit(request, record_id):
    obj = models.Enrollment.objects.filter(pk=record_id).first()
    form_obj = EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment_list', args=('0')))
    return render(request, 'form.html', {'form_obj': form_obj, 'title': '编辑报名记录'})


def enrollment(request, record_id=None, customer_id=None):
    if customer_id:
        obj = models.Enrollment(customer_id=customer_id)
        title = '添加报名记录'
    else:
        obj = models.Enrollment.objects.filter(pk=record_id).first()
        title = '编辑报名记录'
    # obj = models.Enrollment(customer_id=customer_id) if customer_id else models.Enrollment.objects.filter(pk=record_id).first()
    form_obj = EnrollmentForm(instance=obj)
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('enrollment_list', args=('0')))
    # return render(request, 'form.html', {'form_obj': form_obj, 'title': '添加报名记录' if customer_id else '编辑报名记录'})
    return render(request, 'form.html', {'form_obj': form_obj, 'title': title})

