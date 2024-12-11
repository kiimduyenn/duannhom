from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from DIVA.models import YeuCauTuVan, TinNhan, HoiThoai
from ..forms import YCTVForm, SuaYCTVForm, SearchForm, MessageForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import (login_required)
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.db.models import Q, Count
import random

# Create your views here.
def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

def is_admin(user):
    return user.is_superuser

def themyctv(request):
    if request.user.is_superuser or request.user.is_staff:
        layout = 'layout/admin.html'
        h1='Thêm yêu cầu tư vấn'
    else:
        layout = 'layout/customer.html'
        h1='Đăng ký nhận tư vấn'
    yctv=None
    form = YCTVForm(instance=yctv)
    if request.method == 'POST':
        form = YCTVForm(request.POST, instance=yctv)
        if form.is_valid():
            yctv_moi = form.save()
            messages.success(request, f'Yêu cầu của bạn đã được gửi thành công.')
            if request.user.is_superuser or request.user.is_staff:
                return redirect('ql_yctv')
            else:
                return redirect('yctv_cua_toi')
    return render(request, 'yeucautuvan/yctv-form.html', {'form': form, 'yctv': yctv, 'layout':layout,'h1':h1})

@user_passes_test(is_staff_or_admin)
def ql_yctv(request):
    yctv_list = YeuCauTuVan.objects.order_by('MaYCTV')
    search_query = request.GET.get('search', '')
    dich_vu = request.GET.get('dich_vu')
    trang_thai = request.GET.get('trang_thai')
    if dich_vu:
        yctv_list = yctv_list.filter(MaDV=dich_vu)
    if trang_thai:
        yctv_list = yctv_list.filter(TrangThai=trang_thai)
    if search_query:
        yctv_list = YeuCauTuVan.objects.filter(MaYCTV__icontains=search_query)

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
        'dich_vu':dich_vu,
        'trang_thai':trang_thai,
        'search_query': search_query,
    })

@csrf_exempt
@user_passes_test(is_staff_or_admin)
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
@user_passes_test(is_staff_or_admin)
def delete_yctv(request):
    if request.method == "POST":
        MaYCTV = request.POST.get('MaYCTV')
        yc = get_object_or_404(YeuCauTuVan, MaYCTV=MaYCTV)
        yc.delete()
        messages.success(request, f"Yêu cầu {MaYCTV} đã được xóa.")
        return redirect('ql_yctv')
@user_passes_test(is_staff_or_admin)
def yctv_search(request):
    form=SearchForm(request.GET or None )
    if form.is_valid():
        search_text = form.cleaned_data.get('search', '')
        yctv = YeuCauTuVan.objects.filter(title__icontains=search_text)
        context = {'form':form, 'yctv':yctv, 'search_text':search_text}
    return render(request, 'search-results.html', context)

def start_chat(request):
    # Xác định khách hàng
    customer = request.user
    if not customer.is_authenticated:
        return redirect("login")  # Chuyển hướng nếu người dùng chưa đăng nhập

    # Tìm nhân viên hỗ trợ (is_staff=True) có ít cuộc trò chuyện nhất
    employees = User.objects.filter(is_staff=True)
    employees_with_chat_count = employees.annotate(
        chat_count=Count('employee_conversations', filter=Q(employee_conversations__is_active=True))
    ).order_by('chat_count')  # Sắp xếp theo số lượng cuộc trò chuyện

    if not employees_with_chat_count.exists():
        return render(request, 'trangchu/hoithoai_detail.html')  # Hiển thị thông báo nếu không có nhân viên hỗ trợ

    # Chọn nhân viên rảnh nhất
    receiver = employees_with_chat_count.first()

    # Kiểm tra xem đã có cuộc trò chuyện đang hoạt động giữa khách hàng và nhân viên này chưa
    conversation = HoiThoai.objects.filter(customer=customer, employee=receiver, is_active=True).first()
    if not conversation:
        # Tạo cuộc trò chuyện mới
        conversation = HoiThoai.objects.create(customer=customer, employee=receiver)

    # Chuyển hướng đến hộp chat
    return redirect('chat_view', conversation_id=conversation.id)

# View hiển thị cuộc trò chuyện

def chat_view(request, conversation_id):
    # Lấy thông tin cuộc trò chuyện
    conversation = get_object_or_404(HoiThoai, id=conversation_id)

    # Lấy tin nhắn trong cuộc trò chuyện
    messages = TinNhan.objects.filter(conversation=conversation).order_by('timestamp')

    # Xử lý gửi tin nhắn
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = conversation.employee
            message.conversation = conversation
            message.save()
            return redirect('chat_view', conversation_id=conversation.id)
    else:
        form = MessageForm()

    # Render giao diện
    return render(request, 'trangchu/chat.html', {
        'messages': messages,
        'form': form,
        'receiver': conversation.employee
    })

# View hiển thị danh sách các cuộc trò chuyện
def conversations_view(request):
    if request.user.is_superuser or request.user.is_staff:
        layout = 'layout/admin.html'
    else:
        layout = 'layout/customer.html'
    # Lấy danh sách các cuộc trò chuyện của người dùng hiện tại
    user = request.user
    if user.is_staff:  # Nếu là nhân viên hỗ trợ
        conversations = HoiThoai.objects.filter(employee=user).order_by('-created_at')
    else:  # Nếu là khách hàng
        conversations = HoiThoai.objects.filter(customer=user).order_by('-created_at')

    return render(request, 'trangchu/hoithoai.html', {
        'conversations': conversations, 'layout':layout
    })

@login_required
def xem_yctv_cua_toi(request):
    danh_sach_yctv = YeuCauTuVan.objects.filter(SDT=request.user.profile.sodienthoai)
    context = {
        'danh_sach_yctv': danh_sach_yctv,
    }
    return render(request, 'yeucautuvan/xem_yctv_cua_toi.html', context)