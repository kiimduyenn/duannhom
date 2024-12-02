from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from DIVA.models import YeuCauTuVan
from ..forms import YCTVForm, SuaYCTVForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def themyctv(request):
    yctv=None
    form = YCTVForm(instance=yctv)
    if request.method == 'POST':
        form = YCTVForm(request.POST, instance=yctv)
        if form.is_valid():
            yctv_moi = form.save()
            messages.success(request, f'Yêu cầu của bạn đã được gửi thành công.')
            return redirect('ql_yctv')
    return render(request, 'yeucautuvan/yctv-form.html', {'form': form, 'yctv': yctv})

def ql_yctv(request):
    yctv_list = YeuCauTuVan.objects.order_by('MaYCTV')
    user_list = User.objects.filter(is_staff=True)  # Lọc danh sách tài khoản nhân viên

    if request.method == 'POST':
        # Lấy mã yêu cầu từ nút Lưu
        MaYCTV = request.POST.get('MaYCTV')
        trang_thai = request.POST.get('trang_thai')
        nv_phu_trach_id = request.POST.get('nv_phu_trach')

        # Lấy đối tượng yêu cầu tư vấn
        yc = get_object_or_404(YeuCauTuVan, MaYCTV=MaYCTV)

        # Cập nhật trạng thái và nhân viên phụ trách
        if trang_thai:
            yc.TrangThai = trang_thai
        if nv_phu_trach_id:
            yc.MaNV = User.objects.get(id=nv_phu_trach_id) if nv_phu_trach_id else None

        yc.save()  # Lưu thay đổi vào CSDL
        messages.success(request, f"Yêu cầu {MaYCTV} đã được cập nhật thành công!")

        # Redirect để làm mới trang và tránh việc form được gửi lại khi reload
        return redirect('ql_yctv')

    # Hiển thị danh sách yêu cầu và danh sách nhân viên
    return render(request, 'yeucautuvan/ql-yctv.html', {
        'yctv_list': yctv_list,
        'user_list': user_list,
    })

@csrf_exempt
def update_yctv(request):
    if request.method == 'POST':
        ma_yctv = request.POST.get('MaYCTV')
        nv_phu_trach = request.POST.get('nv_phu_trach')
        trang_thai = request.POST.get('trang_thai')

        try:
            yctv = YeuCauTuVan.objects.get(MaYCTV=ma_yctv)
            if nv_phu_trach:
                yctv.MaNV_id = nv_phu_trach  # Cập nhật NV tư vấn
            if trang_thai:
                yctv.TrangThai = trang_thai  # Cập nhật trạng thái
            yctv.save()

            messages.success(request, f"Yêu cầu {ma_yctv} đã được sửa.")
            return redirect('ql_yctv')
        except YeuCauTuVan.DoesNotExist:
            messages.error(request, "Không tìm thấy yctv")
            return redirect('ql_yctv')

def delete_yctv(request):
    if request.method == "POST":
        MaYCTV = request.POST.get('MaYCTV')
        yc = get_object_or_404(YeuCauTuVan, MaYCTV=MaYCTV)
        yc.delete()
        messages.success(request, f"Yêu cầu {MaYCTV} đã được xóa.")
        return redirect('ql_yctv')
def sua_yctv(request, pk):
    yctv=get_object_or_404(YeuCauTuVan,pk=pk)
    form = SuaYCTVForm(instance=yctv)
    if request.method=='POST':
        form=SuaYCTVForm(request.POST, instance=yctv)
        if form.is_valid():
            sua_yctv=form.save()
            messages.success(request, f'Thông tin chỉnh sửa bài viết {sua_yctv.MaYCTV} đã được lưu lại.')
            return redirect('ql_yctv')
    return render(request,'yeucautuvan/sua-yctv.html',{'form':form})