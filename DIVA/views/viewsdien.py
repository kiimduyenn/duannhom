from django.shortcuts import render, get_object_or_404, redirect
from ..models import LichHen
from ..forms import LichHenForm, CapNhatLichHenForm,DangKyForm


def dang_ky(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dang_nhap')  # Sau khi đăng ký thành công, chuyển hướng đến trang đăng nhập
    else:
        form = DangKyForm()

    return render(request, 'auth/dang_ky.html', {'form': form})

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
    # Lấy đối tượng lịch hẹn theo pk
    lich_hen = get_object_or_404(LichHen, pk=pk)

    if request.method == 'POST':
        # Khởi tạo form với dữ liệu POST và đối tượng lịch hẹn hiện tại
        form = CapNhatLichHenForm(request.POST, instance=lich_hen)

        if form.is_valid():  # Kiểm tra tính hợp lệ của form
            form.save()  # Lưu dữ liệu đã cập nhật vào cơ sở dữ liệu
            return redirect('xem_lich_hen')  # Chuyển hướng về trang xem lịch hẹn sau khi lưu thành công
    else:
        form = CapNhatLichHenForm(instance=lich_hen)  # Hiển thị form với dữ liệu lịch hẹn hiện tại

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
