from django.shortcuts import render

from DIVA.models import BaiViet


# Create your views here.
def trangchukh(request):
    bai_viet_list = BaiViet.objects.order_by('-ngay_tao')
    return render(request, 'trangchu/trangchukh.html',{'bai_viet_list': bai_viet_list})
def trangchuad(request):
    return render(request, 'trangchu/trangchuad.html')