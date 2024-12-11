# Generated by Django 4.2.8 on 2024-12-09 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DIVA', '0009_remove_message_receiver_message_is_from_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuocHoiThoai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TinNhan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous_sender', models.CharField(blank=True, max_length=255, null=True)),
                ('noi_dung', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_from_admin', models.BooleanField(default=False)),
                ('cuoc_hoi_thoai', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tin_nhans', to='DIVA.cuochoithoai')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
