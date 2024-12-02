from django.urls import path
from .views import viewsdien, viewsduyen
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dang-ky/', viewsdien.dang_ky, name='dang_ky'),
    path('dang-nhap/', auth_views.LoginView.as_view(template_name='auth/dang_nhap.html'), name='dang_nhap'),
    path('dang-xuat/', auth_views.LogoutView.as_view(next_page='/'), name='dang_xuat'),
    path('lich-hen/', viewsdien.xem_lich_hen, name='xem_lich_hen'),
    path('lich-hen/them/', viewsdien.them_lich_hen, name='them_lich_hen'),
    path('lich-hen/<str:pk>/cap-nhat/', viewsdien.cap_nhat_lich_hen, name='cap_nhat_lich_hen'),
    path('lich-hen/<str:pk>/xoa/', viewsdien.xoa_lich_hen, name='xoa_lich_hen'),








    path('yeu-cau-tu-van/',viewsduyen.themyctv,name='yeu_cau_tu_van'),
    path('ds-yctv/',viewsduyen.ql_yctv,name='ql_yctv'),
    path('sua-yctv/<str:pk>/',viewsduyen.sua_yctv,name='sua_yctv'),
    path('update-yctv/', viewsduyen.update_yctv, name='update_yctv'),
    path('delete-yctv/', viewsduyen.delete_yctv, name='delete_yctv'),

]

