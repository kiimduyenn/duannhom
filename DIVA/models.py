from django.db import models
from django.contrib.auth.models import User

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