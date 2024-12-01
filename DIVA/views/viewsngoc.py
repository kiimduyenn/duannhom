from django.shortcuts import render, get_object_or_404, redirect
from DIVA.models import DichVu
from DIVA.forms import DichVuForm

def danh_sach_dich_vu(request):
    dich_vu_list = DichVu.objects.all()
    return render(request, 'dichvu/danh_sach.html', {'dich_vu_list': dich_vu_list})



def them_dich_vu(request):
    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_dich_vu')
    else:
        form = DichVuForm()
    return render(request, 'dichvu/them.html', {'form': form})

def cap_nhat_dich_vu(request, MaDV):
    dich_vu = get_object_or_404(DichVu, MaDV=MaDV)
    if request.method == 'POST':
        form = DichVuForm(request.POST, instance=dich_vu)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_dich_vu')
    else:
        form = DichVuForm(instance=dich_vu)
    return render(request, 'dichvu/capnhat.html', {'form': form, 'dich_vu': dich_vu})

def xoa_dich_vu(request, MaDV):
    dich_vu = get_object_or_404(DichVu, MaDV=MaDV)
    if request.method == 'POST':
        dich_vu.delete()
        return redirect('danh_sach_dich_vu')
    return render(request, 'dichvu/xoa.html', {'dich_vu': dich_vu})
#hehe

# Create your views here.
