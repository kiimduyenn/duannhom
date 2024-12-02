from django.urls import path
from .views import viewsdien, viewsngoc, viewsnhi, viewshuyen, views, viewsduyen
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dang-ky/', viewsdien.dang_ky, name='dang_ky'),
    path('dang-nhap/', auth_views.LoginView.as_view(template_name='auth/dang_nhap.html'), name='dang_nhap'),
    path('dang-xuat/', auth_views.LogoutView.as_view(next_page='/'), name='dang_xuat'),
    path('lich-hen/', viewsdien.xem_lich_hen, name='xem_lich_hen'),
    path('lich-hen/them/', viewsdien.them_lich_hen, name='them_lich_hen'),
    path('lich-hen/<str:pk>/cap-nhat/', viewsdien.cap_nhat_lich_hen, name='cap_nhat_lich_hen'),
    path('lich-hen/<str:pk>/xoa/', viewsdien.xoa_lich_hen, name='xoa_lich_hen'),
    path('ad/danh-sach-dich-vu/', viewsngoc.danh_sach_dich_vu, name='danh_sach_dich_vu'),
    path('them/', viewsngoc.them_dich_vu, name='them_dich_vu'),
    path('capnhat/<str:MaDV>/', viewsngoc.cap_nhat_dich_vu, name='cap_nhat_dich_vu'),
    path('xoa/<str:MaDV>/', viewsngoc.xoa_dich_vu, name='xoa_dich_vu'),
    path('cus/', viewsnhi.customer, name="customer"),
    path('ds-khach-hang/', viewshuyen.dskhachhang, name='ds_khach_hang'),
    path('thong-tin-khach-hang/<str:username>/', viewshuyen.xemthongtinkhachhang, name='thong_tin_khach_hang'),
    path('khach-hang/', viewshuyen.sua_themthongtinkhachhang, name='them_khach_hang'),
    path('khach-hang/<str:username>/', viewshuyen.sua_themthongtinkhachhang, name='sua_khach_hang'),
    path('xoa-khach-hang/', viewshuyen.xoakhachhang, name='xoa_khach_hang'),

    path('yeu-cau-tu-van/', viewsduyen.themyctv, name='yeu_cau_tu_van'),
    path('ad/ds-yctv/', viewsduyen.ql_yctv, name='ql_yctv'),
    path('sua-yctv/<str:pk>/', viewsduyen.sua_yctv, name='sua_yctv'),
    path('update-yctv/', viewsduyen.update_yctv, name='update_yctv'),
    path('delete-yctv/', viewsduyen.delete_yctv, name='delete_yctv'),
    path('', views.trangchukh, name='trang_chu_kh'),
    path('ad/', views.trangchuad, name='trang_chu_ad'),

]

