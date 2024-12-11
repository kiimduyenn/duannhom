from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now, timedelta
from django.contrib import messages
from DIVA.models import LichHen, DichVu, Profile
from DIVA.forms import LichHenForm, DangKyForm


def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

def is_admin(user):
    return user.is_superuser

def dang_ky(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dang_nhap')
    else:
        form = DangKyForm()

    return render(request, 'auth/dang_ky.html', {'form': form})

# Kiểm tra nếu người dùng là nhân viên
def is_admin(user):
    return user.is_authenticated and user.profile.vaitro == 'Nhân viên'

# Quản lý lịch hẹn của khách hàng
@login_required
def lich_hen_khach_hang(request):
    danh_sach_lich_hen = LichHen.objects.filter(MaKH=request.user)
    return render(request, 'lich_hen/lich_hen_khach_hang.html', {'danh_sach_lich_hen': danh_sach_lich_hen})

# Đăng ký lịch hẹn
@login_required
def dang_ky_lich_hen(request):
    if request.method == 'POST':
        form = LichHenForm(request.POST)
        if form.is_valid():
            lich_hen = form.save(commit=False)
            lich_hen.MaKH = request.user
            lich_hen.TrangThai = 'Chưa xử lý'
            lich_hen.save()
            return redirect('lich_hen_khach_hang')
    else:
        form = LichHenForm()

    danh_sach_dich_vu = DichVu.objects.all()
    return render(request, 'lich_hen/dang_ky_lich_hen.html', {
        'form': form,
        'danh_sach_dich_vu': danh_sach_dich_vu
    })

# Hủy lịch hẹn
@login_required
def huy_lich_hen(request, ma_lich_hen):
    lich_hen = get_object_or_404(LichHen, MaLH=ma_lich_hen, MaKH=request.user)

    if lich_hen.TrangThai in ['Chưa xử lý', 'Đang xử lý']:
        # No need for .date() here as both are date objects
        if lich_hen.thoigiandangki - now().date() > timedelta(days=1):
            lich_hen.TrangThai = 'Đã hủy'
            lich_hen.save()
            messages.success(request, f"Lịch hẹn {ma_lich_hen} đã bị hủy.")
        else:
            messages.error(request, "Không thể hủy lịch hẹn trong vòng 24 giờ.")
    return redirect('lich_hen_khach_hang')

#Quản lý LH
@user_passes_test(is_staff_or_admin)
def quan_ly_lich_hen(request):
    if request.method == "POST":
        ma_lh = request.POST.get('ma_lh')
        action = request.POST.get('action')
        ma_nv = request.POST.get('MaNV')

        try:
            lich_hen = get_object_or_404(LichHen, MaLH=ma_lh)

            # Xử lý hành động "xóa"
            if action == "delete":
                lich_hen.delete()
                messages.success(request, f"Lịch hẹn {ma_lh} đã được xóa.")

            # Gán nhân viên cho lịch hẹn
            elif ma_nv:  # Gán nhân viên phụ trách
                nhan_vien = get_object_or_404(Profile, MaUser__id=ma_nv)
                lich_hen.MaNV = nhan_vien.MaUser
                lich_hen.save()
                messages.success(request, f"Đã gán nhân viên {nhan_vien.MaUser.username} cho lịch hẹn {ma_lh}.")

            # Cập nhật trạng thái
            elif action == "update_status":
                trang_thai_moi = request.POST.get('TrangThai')
                if trang_thai_moi:
                    lich_hen.TrangThai = trang_thai_moi
                    lich_hen.save()
                    messages.success(request, f"Đã cập nhật trạng thái cho lịch hẹn {ma_lh}.")
                    return redirect('quan_ly_lich_hen')
                else:
                    messages.error(request, "Không có trạng thái mới được chọn.")

        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}.")

    # Lấy danh sách lịch hẹn và nhân viên
    danh_sach_lich_hen = LichHen.objects.all()
    danh_sach_nhan_vien = Profile.objects.filter(vaitro='Nhân viên')
    context = {'danh_sach_lich_hen': danh_sach_lich_hen, 'danh_sach_nhan_vien': danh_sach_nhan_vien}
    return render(request, 'lich_hen/quan_ly_lich_hen.html', context)

# Thêm lịch hẹn mới
@user_passes_test(is_staff_or_admin)
def them_lich_hen(request):
    if request.method == 'POST':
        ma_khach_hang = request.POST.get('MaKH')
        ma_dich_vu = request.POST.get('MaDV')
        dich_vu = get_object_or_404(DichVu, MaDV=ma_dich_vu)
        khach_hang = get_object_or_404(Profile, MaUser__username=ma_khach_hang).MaUser
        LichHen.objects.create(
            MaKH=khach_hang,
            MaNV=request.user,
            MaDV=dich_vu,
            thoigiandangki=now(),
            TrangThai='Chưa xử lý'
        )
        return redirect('quan_ly_lich_hen')

    danh_sach_khach_hang = Profile.objects.filter(vaitro='Khách hàng')
    danh_sach_dich_vu = DichVu.objects.all()
    return render(request, 'lich_hen/them_lich_hen.html', {
        'danh_sach_khach_hang': danh_sach_khach_hang,
        'danh_sach_dich_vu': danh_sach_dich_vu
    })
