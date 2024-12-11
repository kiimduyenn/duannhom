from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Tự động tạo Profile khi một User mới được tạo.
    """
    if created:  # Chỉ tạo Profile khi User mới được tạo
        # Xác định vai trò dựa trên nhóm của User
        vaitro = "Nhân viên" if instance.is_staff or instance.is_superuser else "Khách hàng"
        Profile.objects.create(
            MaUser=instance,
            hoten=instance.username,  # Sử dụng username làm tên mặc định
            ngaysinh="2000-01-01",  # Giá trị mặc định
            sodienthoai="0000000000",  # Giá trị mặc định
            diachi="Chưa cập nhật",  # Giá trị mặc định
            vaitro=vaitro  # Vai trò tự động phân loại
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Cập nhật Profile khi User được cập nhật.
    """
    profile = instance.profile
    # Cập nhật vai trò nếu cần
    new_role = "Nhân viên" if instance.is_staff or instance.is_superuser else "Khách hàng"
    if profile.vaitro != new_role:
        profile.vaitro = new_role
        profile.save()
