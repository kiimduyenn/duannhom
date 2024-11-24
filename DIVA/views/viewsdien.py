from django.shortcuts import render, get_object_or_404, redirect
from ..models import LichHen
from ..forms import LichHenForm, CapNhatLichHenForm

def xem_lich_hen(request):
    lich_hen_list = LichHen.objects.filter(MaKH=request.user).order_by('thoigiandangki')
    return render(request, 'lich_hen/xem_lich_hen.html', {'lich_hen_list': lich_hen_list})
def them_lich_hen(request):
    if request.method == 'POST':
        form = LichHenForm(request.POST)
        if form.is_valid():
            lich_hen = form.save(commit=False)  # Tạo đối tượng LichHen nhưng chưa lưu
            lich_hen.MaKH = request.user  # Gán MaKH là khách hàng hiện tại
            lich_hen.save()  # Lưu vào cơ sở dữ liệu
            return redirect('xem_lich_hen')  # Chuyển hướng về trang xem lịch hẹn
    else:
        form = LichHenForm()  # Form để khách hàng điền vào
    return render(request, 'lich_hen/them_lich_hen.html', {'form': form})

def cap_nhat_lich_hen(request, pk):
    lich_hen = get_object_or_404(LichHen, pk=pk)
    if request.method == 'POST':
        form = CapNhatLichHenForm(request.POST, instance=lich_hen)
        if form.is_valid():
            form.save()
            return redirect('xem_lich_hen')
    else:
        form = CapNhatLichHenForm(instance=lich_hen)
    return render(request, 'lich_hen/cap_nhat_lich_hen.html', {'form': form, 'lich_hen': lich_hen})
def xoa_lich_hen(request, pk):
    lich_hen = get_object_or_404(LichHen, pk=pk)
    if request.method == 'POST':
        lich_hen.delete()
        return redirect('xem_lich_hen')
    return render(request, 'lich_hen/xoa_lich_hen.html', {'lich_hen': lich_hen})

def xem_lich_hen(request):
    lich_hen_list = LichHen.objects.filter(MaKH=request.user).order_by('thoigiandangki')
    return render(request, 'lich_hen/xem_lich_hen.html', {'lich_hen_list': lich_hen_list})
