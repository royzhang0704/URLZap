from django.db import models
# Create your models here.

class Url(models.Model):
    origin_url=models.CharField(max_length=2048)
    short_url=models.CharField(max_length=15,unique=True)
    created_at=models.DateField(auto_now_add=True)

    @property

    def __str__(self):
        return self.short_url