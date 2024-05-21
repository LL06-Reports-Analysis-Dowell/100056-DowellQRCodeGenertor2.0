from django.db import models

# Create your models here.

from django.db import models

class QRCode(models.Model):
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"QRCode {self.id}"

class QRCodeClone(models.Model):
    original_qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='clones')
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRCodeClone {self.id}"

class QRCodeVersion(models.Model):
    qrcode = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='versions')
    data = models.TextField()
    version_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRCodeVersion {self.id} v{self.version_number}"



class MasterLink(models.Model):
    name = models.CharField(max_length=255)
    qrcodes = models.ManyToManyField(QRCode, related_name='master_links')
    link = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
