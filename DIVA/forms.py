from django import forms
from .models import LichHen, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DangKyForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class LichHenForm(forms.ModelForm):
    class Meta:
        model = LichHen
        fields = ['MaKH', 'MaNV', 'MaDV', 'thoigiandangki']
        widgets = {
            'thoigiandangki': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'MaKH': 'Khách hàng',
            'MaNV': 'Nhân viên phụ trách',
            'MaDV': 'Dịch vụ',
            'thoigiandangki': 'Ngày đăng ký',
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.MaKH = self.request.user  # Gán MaKH là người dùng hiện tại
            instance.save()
        return instance

class CapNhatLichHenForm(forms.ModelForm):
    class Meta:
        model = LichHen
        fields = ['TrangThai']
        labels = {
            'TrangThai': 'Trạng thái',
        }





class KhachHangForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['MaUser','hoten', 'ngaysinh', 'sodienthoai', 'diachi']
        widgets = {
            'MaUser': forms.Select(attrs={'class': 'form-control'}),
            'hoten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ tên'}),
            'ngaysinh': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sodienthoai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ'}),
        }
        labels = {
            'MaUser': 'Username',
            'hoten': 'Họ tên',
            'ngaysinh': 'Ngày sinh',
            'sodienthoai': 'Số điện thoại',
            'diachi': 'Địa chỉ',
        }
