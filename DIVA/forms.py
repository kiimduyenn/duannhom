from django import forms
from .models import LichHen, Profile, YeuCauTuVan, TinNhan, BaiViet, DichVu, KhieuNai
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class DangKyForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class LichHenForm(forms.ModelForm):
    class Meta:
        model = LichHen
        fields = ['MaDV', 'thoigiandangki']  # Chỉ cần MaDV và thoigiandangki trong form
        thoigiandangki = forms.DateTimeField(initial=now, widget=forms.SelectDateWidget)
        labels = {
            'MaDV': 'Dịch vụ',
            'thoigiandangki': 'Ngày giờ đăng ký',
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        # Gán MaKH là người dùng hiện tại
        instance.MaKH = user
        if commit:
            instance.save()
        return instance

class CapNhatLichHenForm(forms.ModelForm):
    class Meta:
        model = LichHen
        fields = ['TrangThai']
        labels = {
            'TrangThai': 'Trạng thái',
        }

class DichVuForm(forms.ModelForm):
    class Meta:
        model = DichVu
        fields = ['ten', 'giatien', 'mota']

class YCTVForm(forms.ModelForm):
    class Meta:
        model= YeuCauTuVan
        exclude=['MaYCTV','TrangThai', 'MaNV']
        labels = {
            'TenKH': 'Họ tên',
            'SDT': 'Số điện thoại',
            'MaDV': 'Dịch vụ tư vấn',
            'GhiChu': 'Ghi chú'
        }

class SuaYCTVForm(forms.ModelForm):
    class Meta:
        model= YeuCauTuVan
        exclude=['MaYCTV','TenKH', 'SDT','MaDV']
        labels = {
            'TrangThai': 'Trạng Thái',
            'MaNV': 'Nhân viên phụ trách',
        }
class SearchForm(forms.Form):
    search=forms.CharField(required=False, min_length=5)

class MessageForm(forms.ModelForm):
    class Meta:
        model = TinNhan
        fields = ['content']

class BaiVietForm(forms.ModelForm):
    class Meta:
        model = BaiViet
        fields = ['nguoi_tao', 'tieu_de', 'hinh_anh', 'noi_dung', 'thoi_gian_dang']
        widgets = {
            'thoi_gian_dang': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class KhachHangForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['MaUser','hoten', 'ngaysinh', 'sodienthoai', 'diachi', 'DiemTichLuy', 'conversation']
        widgets = {
            'MaUser': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
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

class NhanVienForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['MaUser', 'hoten', 'ngaysinh', 'sodienthoai', 'diachi']
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

class CustomAuthenticationForm(AuthenticationForm):
        def confirm_login_allowed(self, user):
            # Kiểm tra trạng thái khóa từ model Profile
            try:
                profile = Profile.objects.get(MaUser=user)
                if profile.is_locked:
                    raise ValidationError(
                        "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên.",
                        code='locked'
                    )
            except Profile.DoesNotExist:
                # Nếu không có profile liên kết
                raise ValidationError(
                    "Tài khoản này không có hồ sơ người dùng hợp lệ.",
                    code='invalid_profile'
                )

class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['hoten', 'ngaysinh', 'sodienthoai', 'diachi', 'vaitro']
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
class KhieuNaiForm(forms.ModelForm):
    class Meta:
        model = KhieuNai
        fields = ['LoaiKhieuNai', 'NoiDung', 'NgayXayRa']
        widgets = {
            'NgayXayRa': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'LoaiKhieuNai': 'Loại khiếu nại',
            'NoiDung': 'Nội dung khiếu nại',
            'NgayXayRa': 'Ngày xảy ra sự việc',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.MaKH = self.request.user
            instance.save()
        return instance

class CapNhatKhieuNaiForm(forms.ModelForm):
    class Meta:
        model = KhieuNai
        fields = ['TrangThai']
        labels = {
            'TrangThai': 'Trạng thái'
        }