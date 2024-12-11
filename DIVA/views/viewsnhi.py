from django.shortcuts import render, get_object_or_404, redirect
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.http import Http404

# Create your views here.
def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

def is_admin(user):
    return user.is_superuser

def customer(request):
    return render(request,'layout/customer.html')

def admin(request):
    return render(request,'layout/admin.html')

@user_passes_test(is_staff_or_admin)
def xem_khieu_nai(request):
    # Lấy tất cả khiếu nại mà không lọc theo người dùng
    khieu_nai_list = KhieuNai.objects.exclude(MaKN__isnull=True).exclude(MaKN="").order_by('-NgayTiepNhan')
    loai_khieu_nai = request.GET.get('loai_khieu_nai')
    if loai_khieu_nai:
        khieu_nai_list = khieu_nai_list.filter(LoaiKhieuNai=loai_khieu_nai)

    trang_thai = request.GET.get('trang_thai')
    if trang_thai:
        khieu_nai_list = khieu_nai_list.filter(TrangThai=trang_thai)

    ma_kn = request.GET.get('ma_kn')
    if ma_kn:
        khieu_nai_list = khieu_nai_list.filter(MaKN__icontains=ma_kn)

    return render(request, 'khieunai/xem_khieu_nai.html', {'khieu_nai_list': khieu_nai_list})

def them_khieu_nai(request):
    if request.method == 'POST':
        form = KhieuNaiForm(request.POST)
        if form.is_valid():
            khieu_nai = form.save(commit=False)
            khieu_nai.MaKH = request.user
            khieu_nai.save()
            return redirect('khieu_nai_cua_toi')
    else:
        form = KhieuNaiForm()

    return render(request, 'khieunai/them_khieu_nai.html', {'form': form})

@user_passes_test(is_staff_or_admin)
def cap_nhat_khieu_nai(request, pk):

    khieu_nai = get_object_or_404(KhieuNai, pk=pk)

    if request.method == 'POST':

        form = CapNhatKhieuNaiForm(request.POST, instance=khieu_nai)

        if form.is_valid():
            form.save()
            return redirect('xem_khieu_nai')
    else:
        form = CapNhatKhieuNaiForm(instance=khieu_nai)

    return render(request, 'khieunai/cap_nhat_khieu_nai.html', {'form': form, 'khieu_nai': khieu_nai})


@user_passes_test(is_admin)
def xoa_khieu_nai(request, pk):
    if request.method == 'POST':
        khieu_nai = get_object_or_404(KhieuNai, pk=pk)
        ma_kn = khieu_nai.MaKN
        khieu_nai.delete()
        messages.success(request, f'Thông tin khiếu nại của khách hàng "{ma_kn}" đã được xóa thành công!')
        return redirect('xem_khieu_nai')

    return render(request, 'khieunai/xem_khieu_nai.html', {'khieu_nai': get_object_or_404(KhieuNai, pk=pk)})

@user_passes_test(is_staff_or_admin)
def chi_tiet_khieu_nai(request, pk):
    khieunai = get_object_or_404(KhieuNai, MaKN=pk)

    if request.method == 'POST':
        trang_thai = request.POST.get('TrangThai')
        if trang_thai:
            khieunai.TrangThai = trang_thai
            khieunai.save()
            messages.success(request, f'Cập nhật trạng thái "{khieunai.MaKN}" thành công.')
            return redirect('xem_khieu_nai')

    khach_hang = get_object_or_404(Profile, MaUser=khieunai.MaKH)

    context = {
        'MaKN': khieunai.MaKN,
        'hoten': khach_hang.hoten,
        'sodienthoai': khach_hang.sodienthoai,
        'email': khach_hang.MaUser.email,
        'loai_khieu_nai': khieunai.LoaiKhieuNai,
        'ngay_xay_ra': khieunai.NgayXayRa,
        'ngay_tiep_nhan': khieunai.NgayTiepNhan,
        'noi_dung': khieunai.NoiDung,
        'trang_thai': khieunai.TrangThai,
        'nguoi_phu_trach': khieunai.NguoiPhuTrach or "Chưa có",
    }

    return render(request, 'khieunai/chi_tiet_khieu_nai.html', context)


@user_passes_test(is_staff_or_admin)
def diem_tich_luy(request):
    customers = Profile.objects.all()

    if 'search' in request.GET:
        search_term = request.GET['search']
        customers = customers.filter(sodienthoai__icontains=search_term)

    customer_data = []
    for customer in customers:
        diem = DiemTichLuy.objects.filter(MaUser=customer.MaUser).first()
        if not diem:
            dich_vu = DichVu.objects.first()
            diem = DiemTichLuy(MaUser=customer.MaUser, DiemTichLuy=0,
                               NgayTichDiem=timezone.now(), MaDV=dich_vu)
            diem.save()

        customer_data.append({
            'ho_ten': customer.hoten,
            'so_dien_thoai': customer.sodienthoai,
            'diem_tich_luy': diem.DiemTichLuy,
            'MaUser': customer.MaUser,
        })

    if request.method == 'POST' and 'update_points' in request.POST:
        user_id = request.POST.get('user_id')
        new_points = request.POST.get('new_points')

        if user_id and new_points is not None:
            try:
                diem = DiemTichLuy.objects.get(MaUser_id=user_id)
                diem_cu = diem.DiemTichLuy
                diem.DiemTichLuy += int(new_points)
                diem.save()

                customer = Profile.objects.get(MaUser_id=user_id)

                messages.success(request, f'Cập nhật điểm tích lũy cho "{customer.hoten}" thành công!')

                return redirect('diem_tich_luy')

            except ValueError:
                return render(request, 'diem/diem_tich_luy.html',
                              {'customer_data': customer_data, 'error': 'Điểm tích lũy không hợp lệ.'})

    return render(request, 'diem/diem_tich_luy.html', {'customer_data': customer_data})

@login_required
def xem_khieu_nai_cua_toi(request):
    # Lọc các khiếu nại do người dùng hiện tại gửi
    danh_sach_khieu_nai = KhieuNai.objects.filter(MaKH=request.user.profile.MaUser)

    context = {
        'danh_sach_khieu_nai': danh_sach_khieu_nai,
    }

    return render(request, 'khieunai/xem_khieu_nai_cua_toi.html', context)