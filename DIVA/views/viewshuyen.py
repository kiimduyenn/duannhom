from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from DIVA.models import *
from DIVA.forms import KhachHangForm, ProfileForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, logout

# Hàm kiểm tra vai trò nhân viên hoặc admin
def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_staff_or_admin)
def dskhachhang(request):
    # Lấy thông tin từ Profile liên kết với NguoiDung có VaiTro là "Khách hàng"
    profile = Profile.objects.filter(vaitro='Khách hàng', is_Enable=True)
    return render(request, 'quanlykhachhang/dskhachhang.html', {'profile': profile})


@user_passes_test(is_staff_or_admin)
def xemthongtinkhachhang(request, username):
    try:
        # Lấy thông tin người dùng và profile của họ
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(MaUser=user)

        # Trả về thông tin khách hàng cho template
        return render(request, 'quanlykhachhang/thongtinkhachhang.html', {'user': user, 'profile': profile})
    except User.DoesNotExist:
        # Nếu không tìm thấy người dùng
        messages.error(request, "User không tồn tại")
        return HttpResponse("User không tồn tại", status=404)
    except Profile.DoesNotExist:
        # Nếu không tìm thấy profile
        messages.error(request, "Profile không tồn tại")
        return HttpResponse("Profile không tồn tại", status=404)

@user_passes_test(is_staff_or_admin)
def sua_themthongtinkhachhang(request, username=None):
    # Nếu id được truyền, lấy thông tin khách hàng hiện có (sửa)
    if username:
        user = get_object_or_404(User, username=username)
        khach_hang = get_object_or_404(Profile, MaUser=user)
        form = KhachHangForm(instance=khach_hang)
        action = "Cập Nhật"
    else:
        # Nếu không có id, tạo mới (thêm)
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
    # Lấy thông tin profile của user đã đăng nhập
    profile = request.user.profile
    return render(request, 'auth/profile.html', {'profile': profile})

@login_required
def sua_profile(request):
    # Lấy thông tin profile của user hiện tại
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

    return render(request, 'auth/sua_profile.html', {'form': form})


@login_required
def lock_account(request):
    try:
        # Sử dụng MaUser thay cho user
        user_profile = Profile.objects.get(MaUser=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin tài khoản của bạn.")
        return redirect("dang-nhap")

    if request.method == "POST":
        lock_reason = request.POST.get("lock_reason", "").strip()

        if not lock_reason:
            messages.error(request, "Vui lòng nhập lý do khóa tài khoản.")
            return redirect("khoa_taikhoan")

        # Cập nhật thông tin tài khoản
        user_profile.is_locked = True
        user_profile.lock_reason = lock_reason
        user_profile.save()

        # Đăng xuất người dùng
        logout(request)

        # Thông báo thành công và chuyển hướng về trang đăng nhập
        messages.success(request, "Tài khoản của bạn đã bị khóa thành công.")
        return redirect("auth/dang-nhap")

    return render(request, "auth/khoa_taikhoan.html", {"user_profile": user_profile})

# Đăng nhập tùy chỉnh
def custom_login(request, user):
    try:
        # Sử dụng MaUser thay cho user
        user_profile = Profile.objects.get(MaUser=user)
    except Profile.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin tài khoản của bạn.")
        return redirect("dang-nhap")  # Quay về trang đăng nhập nếu không tìm thấy tài khoản

    # Kiểm tra xem tài khoản có bị khóa hay không
    if user_profile.is_locked:
        messages.error(request, "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên để mở khóa.")
        return redirect("dang-nhap")  # Chuyển về trang đăng nhập nếu tài khoản bị khóa

    # Tiến hành đăng nhập nếu tài khoản không bị khóa hoặc bị xóa
    login(request, user)
    return redirect("trang_chu")
