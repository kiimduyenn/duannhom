from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from DIVA.models import *
from DIVA.forms import KhachHangForm, ProfileForm, NhanVienForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from DIVA.forms import CustomAuthenticationForm
from django.urls import reverse_lazy
from django.db.models import Q

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    dang_nhap = 'auth/dang_nhap.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return reverse_lazy('trang_chu_ad')
        else:
            return reverse_lazy('profile')
        return reverse_lazy('profile')

def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_staff_or_admin)
def dskhachhang(request):
    query = request.GET.get('search', '')

    profiles = Profile.objects.filter(vaitro='Khách hàng', is_locked=False)

    if query:
        profiles = profiles.filter(
            Q(hoten__icontains=query) |
            Q(sodienthoai__icontains=query) |
            Q(diachi__icontains=query)
        )

    no_results = profiles.count() == 0

    return render(request, 'quanlykhachhang/dskhachhang.html', {
        'profile': profiles,
        'search': query,
        'no_results': no_results
    })

@user_passes_test(is_staff_or_admin)
def xemthongtinkhachhang(request, username):
    try:
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(MaUser=user)

        return render(request, 'quanlykhachhang/thongtinkhachhang.html', {'user': user, 'profile': profile})
    except User.DoesNotExist:
        messages.error(request, "User không tồn tại")
        return HttpResponse("User không tồn tại", status=404)
    except Profile.DoesNotExist:
        messages.error(request, "Profile không tồn tại")
        return HttpResponse("Profile không tồn tại", status=404)

@user_passes_test(is_staff_or_admin)
def sua_themthongtinkhachhang(request, username=None):
    if username:
        user = get_object_or_404(User, username=username, is_staff=False)
        khach_hang = get_object_or_404(Profile, MaUser=user)
        form = KhachHangForm(instance=khach_hang)
        action = "Cập Nhật"
    else:
        khach_hang = None
        form = KhachHangForm()
        action = "Thêm"

    if request.method == 'POST':
        form = KhachHangForm(request.POST, instance=khach_hang)
        if form.is_valid():
            form.save()
            if action == "Thêm":
                messages.success(request, f'Thêm thông tin khách hàng thành công')
            else:
                messages.success(request, f'{action} thông tin khách hàng thành công')
            return redirect('ds_khach_hang')  # Điều hướng về danh sách khách hàng

    return render(request, 'quanlykhachhang/themkhachhang.html', {'form': form, 'action': action})
@user_passes_test(is_staff_or_admin)
def xoakhachhang(request):
    if request.method == 'POST':
        username = request.POST.get('MaUser')  # Lấy giá trị từ form
        try:
            user = User.objects.get(username=username)
            profile = get_object_or_404(Profile, MaUser=user)  # Hoặc thay MaUser bằng trường khác nếu cần
            profile.delete()
            messages.success(request, f"Thông tin khách hàng {profile.hoten} đã được xóa thành công!")
        except ValueError:
            messages.error(request, "Dữ liệu không hợp lệ. Vui lòng thử lại.")
        return redirect('ds_khach_hang')

@login_required
def xem_profile(request):
    if request.user.is_superuser or request.user.is_staff:
        layout = 'layout/admin.html'
        quan_ly_cv = LichHen.objects.filter(MaKH=request.user).order_by('-thoigiandangki')
    else:
        layout = 'layout/customer.html'
        lich_su = LichHen.objects.filter(MaKH=request.user).order_by('-thoigiandangki')
    profile = request.user.profile
    context = {
        'profile': profile,
        'layout': layout,
        'is_staff': request.user.is_staff,  # Phân biệt nhân viên
        'is_superuser': request.user.is_superuser,  # Phân biệt admin
        'quan_ly_cv': quan_ly_cv if request.user.is_staff else None,
        'lich_su': lich_su if not request.user.is_staff else None,
    }
    return render(request, 'auth/profile.html', context)

@login_required
def sua_profile(request):
    if request.user.is_superuser or request.user.is_staff:
        layout = 'layout/admin.html'
    else:
        layout = 'layout/customer.html'
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Lưu thông tin mới
            messages.success(request, 'Cập nhật thông tin cá nhân thành công.')
            return redirect('profile')  # Quay lại trang profile
        else:
            messages.error(request, 'Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'auth/sua_profile.html', {'form': form, 'layout': layout})


@login_required
def lock_account(request):
    if request.user.is_superuser or request.user.is_staff:
        layout = 'layout/admin.html'
    else:
        layout = 'layout/customer.html'
    try:
        user_profile = Profile.objects.get(MaUser=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin tài khoản của bạn.")
        return redirect("dang_nhap")

    if request.method == "POST":
        lock_reason = request.POST.get("lock_reason", "").strip()

        if not lock_reason:
            messages.error(request, "Vui lòng nhập lý do khóa tài khoản.")
            return redirect("khoa_taikhoan")

        user_profile.is_locked = True
        user_profile.lock_reason = lock_reason
        user_profile.save()

        logout(request)

        messages.success(request, "Tài khoản của bạn đã bị khóa thành công.")
        return redirect("dang_nhap")

    return render(request, "auth/khoa_taikhoan.html", {"user_profile": user_profile, 'layout': layout})

@login_required
def lich_su_sd(request, username=None):
    if username:
        # Admin xem lịch sử của khách hàng cụ thể
        if request.user.is_superuser or request.user.is_staff:
            user = get_object_or_404(User, username=username)
            layout = 'layout/admin.html'
            lich_su = LichHen.objects.filter(MaKH=user).order_by('-thoigiandangki')
        else:
            messages.error(request, "Bạn không có quyền truy cập vào lịch sử này.")
            return redirect('trang_chu_kh')  # Điều hướng về trang khách hàng
    else:
        # Người dùng xem lịch sử của chính mình
        layout = 'layout/customer.html' if not (request.user.is_superuser or request.user.is_staff) else 'layout/admin.html'
        lich_su = LichHen.objects.filter(MaKH=request.user).order_by('-thoigiandangki')

    return render(request, 'auth/lich_su_sd.html', {'lich_su': lich_su, 'layout': layout})

def homepage(request):
    context = {
        "is_authenticated": request.user.is_authenticated,
    }
    return render(request, "trangchu/trangchukh.html", context)

@user_passes_test(is_staff_or_admin)
def dsnhanvien(request):
    query = request.GET.get('search', '')  # Lấy giá trị tìm kiếm từ thanh tìm kiếm

    # Lấy danh sách Profile với VaiTro là "Nhân viên" và không bị khóa
    profiles = Profile.objects.filter(vaitro='Nhân viên', is_locked=False)

    if query:
        # Thêm logic tìm kiếm nếu có từ khóa
        profiles = profiles.filter(
            Q(hoten__icontains=query) |
            Q(sodienthoai__icontains=query) |
            Q(diachi__icontains=query)
        )

    # Kiểm tra nếu không có kết quả tìm kiếm
    no_results = profiles.count() == 0

    return render(request, 'quanlynhanvien/dsnhanvien.html', {
        'profile': profiles,
        'search': query,
        'no_results': no_results
    })

@user_passes_test(is_admin)
def xemthongtinnhanvien(request, username):
    try:
        # Lấy thông tin người dùng và profile của họ
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(MaUser=user)

        # Trả về thông tin khách hàng cho template
        return render(request, 'quanlynhanvien/thongtinnhanvien.html', {'user': user, 'profile': profile})
    except User.DoesNotExist:
        # Nếu không tìm thấy người dùng
        messages.error(request, "User không tồn tại")
        return HttpResponse("User không tồn tại", status=404)
    except Profile.DoesNotExist:
        # Nếu không tìm thấy profile
        messages.error(request, "Profile không tồn tại")
        return HttpResponse("Profile không tồn tại", status=404)

@user_passes_test(is_admin)
def sua_themthongtinnhanvien(request, username=None):
    # Nếu id được truyền, lấy thông tin khách hàng hiện có (sửa)
    if username:
        user = get_object_or_404(User, username=username, is_staff=True)
        nhan_vien = get_object_or_404(Profile, MaUser=user)
        form = NhanVienForm(instance=nhan_vien)
        action = "Cập Nhật"
    else:
        # Nếu không có id, tạo mới (thêm)
        nhan_vien = None
        form = KhachHangForm()
        action = "Thêm"

    if request.method == 'POST':
        form = NhanVienForm(request.POST, instance=nhan_vien)
        if form.is_valid():
            form.save()
            if action == "Thêm":
                messages.success(request, f'Thêm thông tin nhân viên thành công')
            else:
                messages.success(request, f'{action} thông tin nhân viên thành công')
            return redirect('ds_nhan_vien')  # Điều hướng về danh sách khách hàng

    return render(request, 'quanlynhanvien/themnhanvien.html', {'form': form, 'action': action})
@user_passes_test(is_admin)
def xoanhanvien(request):
    if request.method == 'POST':
        username = request.POST.get('MaUser')  # Lấy giá trị từ form
        try:
            user = User.objects.get(username=username)
            profile = get_object_or_404(Profile, MaUser=user)  # Hoặc thay MaUser bằng trường khác nếu cần
            profile.delete()
            messages.success(request, f"Thông tin nhân viên {profile.hoten} đã được xóa thành công!")
        except ValueError:
            messages.error(request, "Dữ liệu không hợp lệ. Vui lòng thử lại.")
        return redirect('ds_nhan_vien')
