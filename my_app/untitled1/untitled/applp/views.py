from django.shortcuts import render, HttpResponse,redirect
from applp import models


def publisher_list(request):
    all_publisher=models.Publisher.objects.all().order_by('pk')
    return render(request, 'publisher_list.html',{'all_publisher':all_publisher})
# Create your views here.
def add_shuju(request):
    err_msg,new_name='',''
    if request.method=='POST':
#获取提交的数据
        new_name=request.POST.get('new_name')
        if not new_name:
            err_msg='不能为空 '
            # return render(request, 'add_shuju.html', {'err_msg': '不能为空 ', 'new_name': new_name})冗余
        objlist = models.Publisher.objects.filter(name=new_name)  # 对象列表
        if objlist:
            err_msg='数据已存在'
            # return render(request, 'add_shuju.html',{'err_msg':'数据已存在','new_name':new_name})冗余
        if new_name and not objlist:
            ret=models.Publisher.objects.create(name=new_name,)
            print(ret)
            return redirect('/publisher_list/')
    return render(request, 'add_shuju.html',  {'err_msg':err_msg, 'new_name': new_name})

def del_shuju(request):
    # '删除功能'
   pk=request.GET.get('pk')
   # print('阿斯蒂芬',pk)
   if not models.Publisher.objects.get(pk=pk):
       return HttpResponse('数据不存在')
   models.Publisher.objects.get(pk=pk).delete()
   return redirect('/publisher_list/')

def edit_shuju(request):
    # 编辑
    pk = request.GET.get('pk')
    objlist = models.Publisher.objects.filter(pk=pk)
    if not objlist:
        return HttpResponse('数据不存在')
    obj = objlist[0]
    return render(request, 'edit_shuju.html',{'obj':obj})

    # all_shuju=models.Publisher.objects.all()

