from django.db import models
from django.conf import settings

STATUS = (
    ('подписан', 'подписан'),
    ('не подписан', 'не подписан'),
)

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='не подписан', choices=STATUS)
    count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name
