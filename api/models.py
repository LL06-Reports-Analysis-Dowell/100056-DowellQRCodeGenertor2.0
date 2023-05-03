from django.db import models

# Create your models here.




class QrCode(models.Model):
    link = models.URLField(max_length=255, blank=True, null=True)
    company_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    logo = models.TextField(blank=True, null=True)
    qrcode = models.TextField(blank=True, null=True)
    logo_size = models.CharField(max_length=255, null=True, blank=True)
    qrcode_color = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company_id
    
    class Meta:
        db_table = 'qrcode'
        verbose_name_plural="QrCodes"
    




   
