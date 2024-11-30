from django.contrib import admin
from DIVA.models import (DichVu, NguoiDung, Profile, LichHen, KhieuNai_LichHen,
                         KhieuNai_DichVu, YeuCauTuVan, DichVuDaDung, YeuCau_DichVu, LichHen_DichVu)


# Register your models here.
admin.site.register(DichVu)
admin.site.register(NguoiDung)
admin.site.register(Profile)
admin.site.register(LichHen)
admin.site.register(KhieuNai_DichVu)
admin.site.register(KhieuNai_LichHen)
admin.site.register(YeuCauTuVan)
admin.site.register(DichVuDaDung)
admin.site.register(YeuCau_DichVu)
admin.site.register(LichHen_DichVu)

