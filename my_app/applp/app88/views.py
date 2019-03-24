import time
from django.shortcuts import render, HttpResponse, redirect
from app88 import models
from django.views import View
from django.utils.decorators import method_decorator

def timer(func):
    def inner(request,*args,**kwargs):
        start=time.time()
        ret =func(*args,**kwargs)
        end=time.time()
        print('时间:{}'.format(end - start))
        return ret
    return inner

class AddPublisher(View):
    # @method_decorator(timer)
    # def dispatch(self, request, *args, **kwargs):
    #     ret = super().dispatch(request, *args, **kwargs)
    #     return ret
    def get(self,request):
        err_msg, new_name = '', ''
        return render(request, 'add_publisher.html', {'err_msg': err_msg, 'new_name': new_name})
    def post(self,request):
        err_msg, new_name = '', ''
        new_name = request.POST.get('new_name')
        print(new_name)
        if not new_name:
            err_msg = '不能为空'
        obj_list = models.Publisher.objects.filter(name=new_name)
        if obj_list:
            err_msg = '数据已存在'
        if new_name and not obj_list:
            ret = models.Publisher.objects.create(name=new_name)
            return redirect('/publisher_list/')
        return render(request, 'add_publisher.html', {'err_msg': err_msg, 'new_name': new_name})
def publisher_list(request):
    all_publisher = models.Publisher.objects.all().order_by('pid')
    return render(request, 'publisher_list.html', {'pubs': all_publisher})
# def add_publisher(request):
#
#     return render(request, 'add_publisher.html', {'err_msg': err_msg, 'new_name': new_name})
def del_publisher(request):
    pk = request.GET.get('pk')
    if not models.Publisher.objects.filter(pk=pk):
        return HttpResponse('数据不存在')
    models.Publisher.objects.get(pk=pk).delete()
    return redirect('/publisher_list/')

def edit_publisher(request):
    err_msg = ''
    pk = request.GET.get('pk')
    obj_list = models.Publisher.objects.filter(pk=pk)
    if not obj_list:
        return HttpResponse('数据不存在')
    obj = obj_list[0]

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if not new_name:
            err_msg = '不能为空'
        exist = models.Publisher.objects.filter(name=new_name)
        if exist:
            err_msg = '数据已存在'
        if new_name and not exist:
            obj.name = new_name
            obj.save()
            return redirect('/publisher_list/')

    return render(request, 'edit_publisher.html', {'obj': obj, 'err_msg': err_msg})
def test(request):
    ret = models.Publisher.objects.filter(name='xx出版社')
    print(ret)
    return HttpResponse('ok')

def book_list(request):
    all_books = models.Book.objects.all()
    # for i in all_books:
    #     print(i.publisher, type(i.publisher))
    #     print(i.publisher_id, )
    #     print(i.publisher.pk, )
    #     print(i.publisher.name, )
    #     print('*' * 20)

    return render(request, 'book_list.html', {'all_books': all_books})



def add_book(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        publisher_id = request.POST.get('publisher_id')
        models.Book.objects.create(title=new_name, publisher_id=publisher_id)
        return redirect('/book_list/')
    all_publishers = models.Publisher.objects.all()
    return render(request, 'add_book.html', {'all_publishers': all_publishers})

def del_book(request):
    pk = request.GET.get('pk')
    models.Book.objects.filter(pk=pk).delete()
    return redirect('/book_list/')


def edit_book(request):
    pk = request.GET.get('pk')
    book_obj = models.Book.objects.get(pk=pk)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        publisher_id = request.POST.get('publisher_id')
        book_obj.title = new_name
        book_obj.publisher_id = publisher_id
        book_obj.save()
        return redirect('/book_list/')
    all_publishers = models.Publisher.objects.all()

    return render(request, 'edit_book.html', {'book_obj': book_obj, 'all_publishers': all_publishers})

def author_list(request):

    all_authors = models.Author.objects.all().order_by('pk')
    return render(request, 'author_list.html', {'all_authors': all_authors})

def add_author(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        book_ids = request.POST.getlist('books')
        author_obj = models.Author.objects.create(name=new_name)
        author_obj.books.set(book_ids)
        return redirect('/author_list/')

    all_books = models.Book.objects.all()
    return render(request, 'add_author.html', {"books": all_books})



def del_author(request):
    del_id = request.GET.get('pk')
    models.Author.objects.get(pk=del_id).delete()
    return redirect('/author_list/')


def edit_author(request):
    pk = request.GET.get('pk')
    author_obj = models.Author.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        book_ids = request.POST.getlist('books')

        author_obj.name = name
        author_obj.save()
        author_obj.books.set(book_ids)

        return redirect('/author_list/')
    books = models.Book.objects.all()

    return render(request, 'edit_author.html', {'author_obj': author_obj, 'books': books})
def add_test(request):
    return render(request, 'add_test.html', {'alex': 123,
                                             'wusir': 'hello',
                                             'taibai':'nice'
                                             })

def add_list(request,table,id):
    table_class=getattr(models,table.capitalize(0))
    table_class.objects.filter(pk=pk).delect()
    return HttpResponse(table)