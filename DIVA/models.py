from django.db import models
from django.contrib.auth.models import User

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
    is_locked = models.BooleanField(null=True, blank=True,default=False)  # Thêm tính năng khóa tài khoản
    lock_reason = models.TextField(null=True, blank=True)  # Thêm lý do khóa tài khoản

    def __str__(self):
        return f"{self.hoten} - {self.vaitro}"

class DichVu(models.Model):
    MaDV = models.CharField(max_length=10, primary_key=True)
    ten = models.CharField(max_length=100)
    giatien = models.DecimalField(max_digits=10, decimal_places=2)
    mota = models.TextField()

    def __str__(self):
        return self.ten

class LichHen(models.Model):
    TrangThai_CHOICES = [
        ('pending', 'Chưa xử lý'),
        ('processing', 'Đang xử lý'),
        ('completed', 'Đã hoàn thành'),
        ('canceled', 'Đã hủy'),
    ]
    MaLH = models.CharField(max_length=10, primary_key=True, editable=False)
    MaKH = models.ForeignKey(User, on_delete=models.CASCADE, related_name='KH_LichHen')
    MaNV = models.ForeignKey(User, on_delete=models.CASCADE, related_name='NV_LichHen')
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
        ('Đang xử lý', 'Đang xử lý'),
        ('Tư vấn lại', 'Tư vấn lại'),
    ]
    MaYCTV = models.CharField(max_length=10, primary_key=True, editable=False)
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)
    TenKH = models.CharField(max_length=100)
    SDT = models.CharField(max_length=10)
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

class KhieuNai_DichVu(models.Model):
    MaKH=models.CharField(max_length=10,primary_key=True)
    noidung=models.TextField()
    trangthaixuly=models.CharField(max_length=10,
                choices=[('Chua','Chưa xử lý'),('Dang','Đang xử lý'),('Da','Đã xử lý')])
    def __str__(self):
        return f'{self.MaKH}-{self.trangthaixuly}'

class KhieuNai_LichHen(models.Model):
    TrangThai_CHOICES = [
        ('Chưa xử lý', 'Chưa xử lý'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Đã hoàn thành', 'Đã hoàn thành'),
    ]
    MaKN = models.CharField(max_length=10, primary_key=True, editable=False)
    MaKH = models.ForeignKey(User, on_delete=models.CASCADE, related_name='KH_KNLH')
    MaLH = models.ForeignKey(LichHen, on_delete=models.CASCADE)
    MaNV = models.ForeignKey(User, on_delete=models.CASCADE, related_name='NV_KNLH')
    NoiDung = models.TextField()
    TrangThai = models.CharField(max_length=20, choices=TrangThai_CHOICES, default='Chưa xử lý')

    def save(self, *args, **kwargs):
        if not self.MaKN:
            last_knlh = KhieuNai_LichHen.objects.order_by('MaKN').last()
            if last_knlh:
                last_id = int(last_knlh.MaLH[2:])  # Lấy số từ "LH001"
                self.MaKN = f"LH{last_id + 1:03d}"  # Tạo mã mới
            else:
                self.MaKN = "LH001"  # Mã đầu tiên
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.MaKN} - {self.TrangThai}"
    def is_completed(self):
        return self.TrangThai == 'Đã hoàn thành'

class DichVuDaDung(models.Model):
    MaUser=models.ForeignKey(User,on_delete=models.CASCADE)
    MaDV=models.ForeignKey(DichVu,on_delete=models.CASCADE)
    MaKN=models.ForeignKey(KhieuNai_DichVu,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.MaUser} - {self.DichVu.ten}'

class YeuCau_DichVu(models.Model):
    MaYCTV=models.ForeignKey(YeuCauTuVan,on_delete=models.CASCADE)
    MaDV=models.ForeignKey(DichVu,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.YeuCauTuVan.TenKH} - {self.DichVu.ten}'

class LichHen_DichVu(models.Model):
    MaLH = models.ForeignKey(LichHen, on_delete=models.CASCADE)
    MaDV = models.ForeignKey(DichVu, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.DichVu.ten} - {self.LichHen.thoigiandangki}'
