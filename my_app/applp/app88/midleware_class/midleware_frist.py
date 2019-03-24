# from django.utils.deprecation import MiddlewareMixin


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect


class Md1(MiddlewareMixin):
    white_list=['/login/']
    back_list=['/publisher_list/']
    def process_request(self,request):
        next_url=request.path_info
        print(request.path_info,request.get_full_path())
        print('请求',request)
        print('毛里求斯')
        if next_url in self.back_list:
            return HttpResponse('not')
        elif next_url in self.white_list or request.session.get('user'):
            return
        else:
            return redirect('   /login/?next={}'.format(next_url   ))

        # return HttpResponse('hello')
