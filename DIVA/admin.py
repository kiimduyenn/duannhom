from django.contrib import admin
from DIVA.models import (DichVu, Profile, LichHen, KhieuNai , YeuCauTuVan, DichVuDaDung, YeuCau_DichVu, LichHen_DichVu, TinNhan, HoiThoai,
                         TinNhan, BaiViet)


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('MaUser', 'hoten', 'ngaysinh', 'sodienthoai', 'diachi', 'vaitro', 'is_locked', 'lock_reason')
    search_fields = ('MaUser__username', 'hoten')

    def delete_model(self, request, obj):
        obj.delete()

admin.site.register(DichVu)
admin.site.register(LichHen)
admin.site.register(KhieuNai)
admin.site.register(YeuCauTuVan)
admin.site.register(DichVuDaDung)
admin.site.register(YeuCau_DichVu)
admin.site.register(LichHen_DichVu)
admin.site.register(TinNhan)
admin.site.register(HoiThoai)
admin.site.register(BaiViet)
