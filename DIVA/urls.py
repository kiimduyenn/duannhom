from django.conf.urls.static import static
from django.urls import path
from DIVA.views.viewshuyen import CustomLoginView
from duannhom import settings
from .views import viewsdien, viewsngoc, viewsnhi, viewshuyen, views, viewsduyen
from django.contrib.auth import views as auth_views
#ý là mấy file thư viện này nè, bạn tải về máy hả đúng
urlpatterns = ([
    path('dang-ky/', viewsdien.dang_ky, name='dang_ky'),
    path('dang-xuat/', auth_views.LogoutView.as_view(next_page='/'), name='dang_xuat'),
    path('ad/danh-sach-dich-vu/', viewsngoc.danh_sach_dich_vu, name='danh_sach_dich_vu'),
    path('them/', viewsngoc.them_dich_vu, name='them_dich_vu'),
    path('capnhat/<str:MaDV>/', viewsngoc.cap_nhat_dich_vu, name='cap_nhat_dich_vu'),
    path('xoa/<str:MaDV>/', viewsngoc.xoa_dich_vu, name='xoa_dich_vu'),
    path('yeu-cau-tu-van/', viewsduyen.themyctv, name='yeu_cau_tu_van'),
    path('ad/ds-yctv/', viewsduyen.ql_yctv, name='ql_yctv'),
    path('ad/them-yctv/', viewsduyen.themyctv, name='them_yctv_nv'),
    path('update-yctv/', viewsduyen.update_yctv, name='update_yctv'),
    path('delete-yctv/', viewsduyen.delete_yctv, name='delete_yctv'),
    path('', views.trangchukh, name='trang_chu_kh'),
    path('ad/', views.trangchuad, name='trang_chu_ad'),
    path('conversations/', viewsduyen.conversations_view, name='conversations'),
    path('chat/<int:conversation_id>/', viewsduyen.chat_view, name='chat_view'),
    path('start-chat/', viewsduyen.start_chat, name='start_chat'),
    path('danh-sach-bai-viet/', viewsngoc.danh_sach_bai_viet, name='danh_sach_bai_viet'),
    path('ad/tao-bai-viet/', viewsngoc.tao_bai_viet, name='tao_bai_viet'),
    path('bai-viet/<int:bai_viet_id>/', viewsngoc.chi_tiet_bai_viet, name='chi_tiet_bai_viet'),
    path('ve-chung-toi/', viewsngoc.ve_chung_toi, name='ve_chung_toi'),

    path('lich-hen/', viewsdien.lich_hen_khach_hang, name='lich_hen_khach_hang'),
    path('lich-hen/dang-ky/', viewsdien.dang_ky_lich_hen, name='dang_ky_lich_hen'),
    path('lich-hen/huy/<str:ma_lich_hen>/', viewsdien.huy_lich_hen, name='huy_lich_hen'),
    path('ad/lich-hen/', viewsdien.quan_ly_lich_hen, name='quan_ly_lich_hen'),
    path('ad/lich-hen/xoa/<str:ma_lich_hen>/', viewsdien.huy_lich_hen, name='xoa_lich_hen'),
    path('ad/lich-hen/them/', viewsdien.them_lich_hen, name='them_lich_hen'),

    path('ad/ds-khach-hang/', viewshuyen.dskhachhang, name='ds_khach_hang'),
    path('ad/thong-tin-khach-hang/<str:username>/', viewshuyen.xemthongtinkhachhang, name='thong_tin_khach_hang'),
    path('ad/khach-hang/', viewshuyen.sua_themthongtinkhachhang, name='them_khach_hang'),
    path('ad/khach-hang/<str:username>/', viewshuyen.sua_themthongtinkhachhang, name='sua_khach_hang'),
    path('ad/xoa-khach-hang/', viewshuyen.xoakhachhang, name='xoa_khach_hang'),
    path('profile/', viewshuyen.xem_profile, name='profile'),
    path('sua-profile/', viewshuyen.sua_profile, name='sua_profile'),
    path('khoa-taikhoan/', viewshuyen.lock_account, name='khoa_taikhoan'),
    path('dang-nhap/', CustomLoginView.as_view(template_name='auth/dang_nhap.html'), name='dang_nhap'),
    path('lich_su_sd/', viewshuyen.lich_su_sd, name='lich_su_sd'),
    path('quan_ly_cv/<str:username>/', viewshuyen.quan_ly_cv, name='quan_ly_cv'),
    path('quan_ly_cv/', viewshuyen.quan_ly_cv, name='quan_ly_cv'),
    path('lich_su_sd/<str:username>/', viewshuyen.lich_su_sd, name='lich_su_kh'),
    path('ad/ds-nhan-vien/', viewshuyen.dsnhanvien, name='ds_nhan_vien'),
    path('ad/thong-tin-nhan-vien/<str:username>/', viewshuyen.xemthongtinnhanvien, name='thong_tin_nhan_vien'),
    path('ad/nhan-vien/', viewshuyen.sua_themthongtinnhanvien, name='them_nhan_vien'),
    path('ad/nhan-vien/<str:username>/', viewshuyen.sua_themthongtinnhanvien, name='sua_nhan_vien'),
    path('ad/xoa-nhan-vien/', viewshuyen.xoanhanvien, name='xoa_nhan_vien'),

    path('them-khieu-nai/', viewsnhi.them_khieu_nai, name='them_khieu_nai'),
    path('ad/xem-khieu-nai/', viewsnhi.xem_khieu_nai, name='xem_khieu_nai'),
    path('khieu-nai/<str:pk>/cap-nhat/', viewsnhi.cap_nhat_khieu_nai, name='cap_nhat_khieu_nai'),
    path('khieu-nai/<str:pk>/xoa/', viewsnhi.xoa_khieu_nai, name='xoa_khieu_nai'),
    path('khieu-nai/chi-tiet/<str:pk>/', viewsnhi.chi_tiet_khieu_nai, name='chi_tiet_khieu_nai'),
    path('diem-tich-luy/', viewsnhi.diem_tich_luy, name='diem_tich_luy'),
    path('khieu-nai-cua-toi/', viewsnhi.xem_khieu_nai_cua_toi, name='khieu_nai_cua_toi'),
    path('yctv-cua-toi/', viewsduyen.xem_yctv_cua_toi, name='yctv_cua_toi'),
]
+ static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)) if settings.DEBUG else []

