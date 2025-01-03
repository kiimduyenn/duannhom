# Generated by Django 4.2.8 on 2024-12-11 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DIVA', '0016_diemtichluy_khieunai_delete_khieunai_lichhen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='DiemTichLuy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DIVA.diemtichluy'),
        ),
        migrations.AddField(
            model_name='profile',
            name='conversation',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hoithoai', to='DIVA.hoithoai'),
        ),
    ]
