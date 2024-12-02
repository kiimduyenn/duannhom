# Generated by Django 4.2.8 on 2024-12-02 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DIVA', '0003_alter_yeucautuvan_manv'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='vaitro',
            field=models.CharField(choices=[('Nhân viên', 'Nhân viên'), ('Khách hàng', 'Khách hàng')], default='Khách hàng', max_length=20),
        ),
        migrations.AlterField(
            model_name='dichvudadung',
            name='MaUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='khieunai_lichhen',
            name='MaKH',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='KH_KNLH', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='khieunai_lichhen',
            name='MaNV',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='NV_KNLH', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='MaUser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_Enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sodienthoai',
            field=models.CharField(max_length=10),
        ),
        migrations.DeleteModel(
            name='NguoiDung',
        ),
    ]