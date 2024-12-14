from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DichVu(models.Model):
    MaDV = models.CharField(max_length=10, primary_key=True)
    ten = models.CharField(max_length=100)
    giatien = models.DecimalField(max_digits=10, decimal_places=2)
    mota = models.TextField()

    def __str__(self):
        return self.ten

    def save(self, *args, **kwargs):
        # Tạo MaDV tự động khi chưa có MaDV
        if not self.MaDV:
            last_dv = DichVu.objects.order_by('MaDV').last()  # Lấy bản ghi cuối cùng
            if last_dv:
                last_id = int(last_dv.MaDV[2:])  # Lấy số từ phần MaDV
                self.MaDV = f"DV{last_id + 1:03d}"  # Tạo MaDV mới
            else:
                self.MaDV = "DV001"  # Mã đầu tiên là "DV001"
        super().save(*args, **kwargs)

class LichHen(models.Model):
    TrangThai_CHOICES = [
        ('pending', 'Chưa xử lý'),
        ('processing', 'Đang xử lý'),
        ('completed', 'Đã hoàn thành'),
        ('canceled', 'Đã hủy'),
    ]
    MaLH = models.CharField(max_length=10, primary_key=True, editable=False)
    MaKH = models.ForeignKey(User, on_delete=models.CASCADE, related_name='KH_LichHen')
    MaNV = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='NV_LichHen')
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)
    thoigiandangki = models.DateField()
    TrangThai = models.CharField(max_length=20, choices=TrangThai_CHOICES, default='pending')

    class Meta:
        ordering = ['thoigiandangki']  # Sắp xếp theo ngày đăng ký

    def save(self, *args, **kwargs):
        if not self.MaLH:
            last_lh = LichHen.objects.order_by('MaLH').last()
            if last_lh:
                last_id = int(last_lh.MaLH[2:])  # Lấy số từ "LH001"
                self.MaLH = f"LH{last_id + 1:03d}"  # Tạo mã mới
            else:
                self.MaLH = "LH001"  # Mã đầu tiên
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.MaLH} - {self.TrangThai}"

    def is_completed(self):
        return self.TrangThai == 'completed'

    def is_canceled(self):
        return self.TrangThai == 'canceled'

class YeuCauTuVan(models.Model):
    TrangThai_CHOICES = [
        ('Chưa xử lý', 'Chưa xử lý'),
        ('Đã tư vấn', 'Đã tư vấn'),
        ('Tư vấn lại', 'Tư vấn lại'),
    ]
    MaYCTV = models.CharField(max_length=10, primary_key=True, editable=False)
    TenKH = models.CharField(max_length=100)
    SDT = models.CharField(max_length=10)
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)
    GhiChu = models.TextField(blank=True, null=True)
    MaNV = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='NV_YCTV')
    TrangThai = models.CharField(max_length=20, choices=TrangThai_CHOICES, default='Chưa xử lý')

    def save(self, *args, **kwargs):
        if not self.MaYCTV:
            last_yctv = YeuCauTuVan.objects.order_by('MaYCTV').last()
            if last_yctv:
                last_id = int(last_yctv.MaYCTV[2:])  # Lấy số từ "LH001"
                self.MaYCTV = f"YC{last_id + 1:03d}"  # Tạo mã mới
            else:
                self.MaYCTV = "YC001"  # Mã đầu tiên
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.MaYCTV} - {self.TrangThai}"


class KhieuNai(models.Model):
    LOAI_KHIEU_NAI_CHOICES = [
        ('Dịch Vụ', 'Dịch vụ'),
        ('Lịch Hẹn', 'Lịch hẹn'),
    ]
    TrangThai_CHOICES = [
        ('Chưa xử lý', 'Chưa xử lý'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Đã hoàn thành', 'Đã hoàn thành'),
    ]

    MaKN = models.CharField(max_length=10, primary_key=True, editable=False)
    MaKH = models.ForeignKey(User, on_delete=models.CASCADE, related_name='KH_KN')
    LoaiKhieuNai = models.CharField(max_length=10, choices=LOAI_KHIEU_NAI_CHOICES,
                                    default='DichVu')

    MaNV = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='NV_KN')

    NoiDung = models.TextField()
    NgayXayRa = models.DateField()
    TrangThai = models.CharField(max_length=20, choices=TrangThai_CHOICES, default='Chưa xử lý')
    NgayTiepNhan = models.DateField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if not self.MaKN:
            last_kn = KhieuNai.objects.order_by('MaKN').last()
            if last_kn and len(last_kn.MaKN) > 2:
                try:
                    last_id = int(last_kn.MaKN[2:])
                    self.MaKN = f"KN{last_id + 1:03d}"
                except ValueError:

                    self.MaKN = "KN001"
            else:
                self.MaKN = "KN001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.MaKN} - {self.TrangThai}"


class DiemTichLuy(models.Model):
    MaUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diem_tich_luy')
    DiemTichLuy = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"User: {self.MaUser} - Điểm: {self.DiemTichLuy}"


class DichVuDaDung(models.Model):
    MaUser = models.ForeignKey(User, on_delete=models.CASCADE)
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)
    MaKN = models.ForeignKey(KhieuNai, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.MaUser} - {self.DichVu.ten}'

class YeuCau_DichVu(models.Model):
    MaYCTV = models.ForeignKey(YeuCauTuVan, on_delete=models.CASCADE)
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.YeuCauTuVan.TenKH} - {self.DichVu.ten}'

class LichHen_DichVu(models.Model):
    MaLH = models.ForeignKey(LichHen, on_delete=models.CASCADE)
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)

    def __str__(self):
          return f'{self.DichVu.ten} - {self.LichHen.thoigiandangki}'

class HoiThoai(models.Model):
    customer = models.ForeignKey(User, related_name="customer_conversations", on_delete=models.CASCADE)
    employee = models.ForeignKey(User, related_name="employee_conversations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
       return f"Conversation between {self.customer.username} and {self.employee.username}"

class TinNhan(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(HoiThoai, related_name="messages", on_delete=models.CASCADE, null=True,
                                             blank=True, default=None)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class BaiViet(models.Model):
    nguoi_tao = models.CharField(max_length=500)
    tieu_de = models.CharField(max_length=500)
    hinh_anh = models.ImageField(upload_to='')
    noi_dung = models.FileField(upload_to='uploads/', null=True, blank=True)  # File
    ngay_tao = models.DateField(auto_now_add=True)
    thoi_gian_dang = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.tieu_de
class Profile(models.Model):
    VaiTro_CHOICES = [
        ('Nhân viên', 'Nhân viên'),
        ('Khách hàng', 'Khách hàng'),
    ]
    MaUser = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hoten=models.CharField(max_length=50)
    ngaysinh=models.DateField()
    sodienthoai=models.CharField(max_length=10)
    diachi=models.CharField(max_length=120)
    vaitro = models.CharField(max_length=20, choices=VaiTro_CHOICES, default='Khách hàng')
    is_locked = models.BooleanField(null=True, blank=True,default=False)
    lock_reason = models.TextField(null=True, blank=True)
    conversation = models.ForeignKey(HoiThoai, related_name="hoithoai", on_delete=models.CASCADE, null=True,
                                     blank=True, default=None)

    def __str__(self):
        return f"{self.hoten} - {self.vaitro}"
