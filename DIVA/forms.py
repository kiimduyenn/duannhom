from django import forms
from .models import LichHen, Profile, YeuCauTuVan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

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
from .models import DichVu

class DichVuForm(forms.ModelForm):
    class Meta:
        model = DichVu
        fields = ['MaDV', 'ten', 'giatien', 'mota']

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

class YCTVForm(forms.ModelForm):
    class Meta:
        model= YeuCauTuVan
        exclude=['MaYCTV','TrangThai', 'MaNV']
        labels = {
            'TenKH': 'Họ tên',
            'SDT': 'Số điện thoại',
            'MaDV': 'Dịch vụ tư vấn'
        }

class SuaYCTVForm(forms.ModelForm):
    class Meta:
        model= YeuCauTuVan
        exclude=['MaYCTV','TenKH', 'SDT','MaDV']
        labels = {
            'TrangThai': 'Trạng Thái',
            'MaNV': 'Nhân viên phụ trách',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['hoten', 'ngaysinh', 'sodienthoai', 'diachi','vaitro']
        widgets = {
            'hoten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ tên'}),
            'ngaysinh': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sodienthoai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ'}),
            'vaitro': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        labels = {
            'hoten': 'Họ tên',
            'ngaysinh': 'Ngày sinh',
            'sodienthoai': 'Số điện thoại',
            'diachi': 'Địa chỉ',
            'vaitro': 'Vai trò'
        }


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Tài khoản của bạn đã bị vô hiệu hóa. Vui lòng liên hệ quản trị viên.",
                code='inactive',
            )
        if hasattr(user, 'is_locked') and user.is_locked:
            raise forms.ValidationError(
                f"Tài khoản của bạn đã bị khóa: {user.lock_reason}",
                code='locked',
            )