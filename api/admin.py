from django.contrib import admin
from .models import QrCode

class QrCodeAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'link', 'logo_size', 'qrcode_color', 'is_active']
    list_filter = ('company_id',)
    
    ordering = ["company_id"]

admin.site.register(QrCode, QrCodeAdmin)


