from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Mỗi khi một User mới được tạo, tự động tạo Profile tương ứng.
    """
    if created:  # Chỉ tạo Profile khi User mới được tạo
        Profile.objects.create(
            MaUser=instance,
            hoten=instance.username,  # Sử dụng username làm tên mặc định
            ngaysinh="2000-01-01",  # Giá trị mặc định
            sodienthoai=0,  # Giá trị mặc định
            diachi="Chưa cập nhật",  # Giá trị mặc định
            is_Enable=True,  # Giá trị mặc định
            vaitro="Khách hàng"  # Giá trị mặc định
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Lưu Profile khi User được cập nhật.
    """
    instance.profile.save()
